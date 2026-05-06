/*
 * abrir_links.c
 *
 * Exemplo de utilitário em C para vasculhar pastas, encontrar links em arquivos
 * Markdown e listá-los (ou abrir no navegador).
 *
 * Uso:
 *   gcc -o abrir_links abrir_links.c
 *   abrir_links           -> vasculha diretório atual e lista links
 *   abrir_links --open    -> abre os links no navegador padrão (Windows)
 *   abrir_links <pasta>   -> vasculha a pasta especificada
 *
 * Observação:
 * - Esta versão foi feita para Windows (usa _findfirst/_findnext e ShellExecuteA).
 * - Para compilação com MSVC: cl /Fe:abrir_links abrir_links.c
 */

#ifdef _WIN32
#define _CRT_SECURE_NO_WARNINGS
#include <windows.h>
#include <shellapi.h>
#include <io.h>
#else
#include <dirent.h>
#endif

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 4096

static int stricmp_local(const char *a, const char *b)
{
  while (*a && *b)
  {
    char ca = (char)tolower((unsigned char)*a);
    char cb = (char)tolower((unsigned char)*b);
    if (ca != cb)
      return (unsigned char)ca - (unsigned char)cb;
    a++;
    b++;
  }
  return (unsigned char)tolower((unsigned char)*a) - (unsigned char)tolower((unsigned char)*b);
}

static int strnicmp_local(const char *a, const char *b, size_t n)
{
  while (n-- && *a && *b)
  {
    char ca = (char)tolower((unsigned char)*a);
    char cb = (char)tolower((unsigned char)*b);
    if (ca != cb)
      return (unsigned char)ca - (unsigned char)cb;
    a++;
    b++;
  }
  return 0;
}

static bool ends_with(const char *str, const char *suffix)
{
  if (!str || !suffix)
    return false;
  size_t lenstr = strlen(str);
  size_t lensuf = strlen(suffix);
  if (lensuf > lenstr)
    return false;
  return stricmp_local(str + lenstr - lensuf, suffix) == 0;
}

static void abrir_link_no_navegador(const char *link)
{
#ifdef _WIN32
  ShellExecuteA(NULL, "open", link, NULL, NULL, SW_SHOWNORMAL);
#else
  /* Em WSL, use cmd.exe para abrir no navegador do Windows */
  char cmd[1024];
  if (system(NULL))
  {
    snprintf(cmd, sizeof(cmd), "cmd.exe /c start \"\" \"%s\"", link);
    system(cmd);
  }
#endif
}

static void processar_linha_para_links(const char *linha, const char *arquivo, bool abrir)
{
  const char *p = linha;

  /* 1) Formato "AULA: http..." */
  if (strnicmp_local(p, "AULA", 4) == 0)
  {
    const char *c = strchr(p, ':');
    if (c)
    {
      while (*c && isspace((unsigned char)*c))
        c++;
      if (strncmp(c, "http://", 7) == 0 || strncmp(c, "https://", 8) == 0)
      {
        printf("%s -> %s\n", arquivo, c);
        if (abrir)
          abrir_link_no_navegador(c);
      }
    }
    return;
  }

  /* 2) Links com http:// ou https:// em qualquer parte da linha */
  while (*p)
  {
    const char *http_pos = strstr(p, "http://");
    const char *https_pos = strstr(p, "https://");
    const char *start = NULL;

    if (http_pos && (!https_pos || http_pos < https_pos))
      start = http_pos;
    else if (https_pos)
      start = https_pos;
    else
      break;

    const char *end = start;
    while (*end && *end != '"' && *end != '\'' && *end != ' ' && *end != '<' && *end != '>')
    {
      end++;
    }
    size_t len = end - start;
    if (len > 0 && len < 2000)
    {
      char link[2048];
      if (len >= sizeof(link))
        len = sizeof(link) - 1;
      memcpy(link, start, len);
      link[len] = '\0';
      printf("%s -> %s\n", arquivo, link);
      if (abrir)
        abrir_link_no_navegador(link);
    }
    p = end;
  }
}

static void processar_arquivo_md(const char *caminho, bool abrir)
{
  FILE *f = fopen(caminho, "r");
  if (!f)
    return;

  char linha[MAX_LINE];
  while (fgets(linha, sizeof(linha), f))
  {
    processar_linha_para_links(linha, caminho, abrir);
  }

  fclose(f);
}

#ifdef _WIN32
static void scan_dir(const char *dir, bool abrir)
{
  char pattern[MAX_PATH];
  snprintf(pattern, sizeof(pattern), "%s\\*", dir);

  struct _finddata_t info;
  intptr_t h = _findfirst(pattern, &info);
  if (h == -1)
    return;

  do
  {
    if (strcmp(info.name, ".") == 0 || strcmp(info.name, "..") == 0)
      continue;

    char full[MAX_PATH];
    snprintf(full, sizeof(full), "%s\\%s", dir, info.name);

    if (info.attrib & _A_SUBDIR)
    {
      scan_dir(full, abrir);
    }
    else
    {
      if (ends_with(info.name, ".md") || ends_with(info.name, ".markdown"))
      {
        processar_arquivo_md(full, abrir);
      }
    }
  } while (_findnext(h, &info) == 0);

  _findclose(h);
}
#else
static void scan_dir(const char *dir, bool abrir)
{
  DIR *d = opendir(dir);
  if (!d)
    return;

  struct dirent *ent;
  while ((ent = readdir(d)) != NULL)
  {
    if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0)
      continue;

    char full[4096];
    snprintf(full, sizeof(full), "%s/%s", dir, ent->d_name);

    if (ent->d_type == DT_DIR)
    {
      scan_dir(full, abrir);
    }
    else if (ent->d_type == DT_REG)
    {
      if (ends_with(ent->d_name, ".md") || ends_with(ent->d_name, ".markdown"))
      {
        processar_arquivo_md(full, abrir);
      }
    }
  }

  closedir(d);
}
#endif

int main(int argc, char **argv)
{
  bool abrir = false;
  const char *raiz = ".";

  for (int i = 1; i < argc; ++i)
  {
    if (strcmp(argv[i], "--open") == 0 || strcmp(argv[i], "-o") == 0)
    {
      abrir = true;
    }
    else
    {
      raiz = argv[i];
    }
  }

  scan_dir(raiz, abrir);

  return 0;
}
