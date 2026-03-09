# Quick file/dir inspection
alias ll='ls -lah'
alias dus='du -sh .'
alias du1='du -sh *'
alias countf='find . -maxdepth 1 -type f | wc -l'
alias counta='ls -1A | wc -l'

inspecthelp() {
  echo ""
  echo "Common inspection commands:"
  echo "  ll       -> ls -lah"
  echo "  dus      -> du -sh ."
  echo "  du1      -> du -sh *"
  echo "  countf   -> count files in current dir"
  echo "  counta   -> count all entries in current dir"
  echo ""
}

inspect() {
  echo ""
  echo "Path: $(pwd)"
  echo "----------------------------------------"
  echo "[entries]"
  ls -lah
  echo ""
  echo "[total size]"
  du -sh .
  echo ""
  echo "[size of each item]"
  du -sh * 2>/dev/null
  echo ""
  echo "[file count]"
  find . -maxdepth 1 -type f | wc -l
  echo ""
  echo "[entry count]"
  ls -1A | wc -l
  echo ""
}
