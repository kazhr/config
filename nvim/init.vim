" --
" initialize (deinより前に書く)
augroup my_group
  au!
augroup END

" --
" load dein
if has('nvim') && filereadable(expand('<sfile>:p:h').'/dein.vim')
    source <sfile>:p:h/dein.vim
endif

" --
" enable auto-indenting & highlight
filetype plugin indent on
syntax enable

" --
" ubuntuでのバグ回避(https://github.com/neovim/neovim/issues/6403)
"let $NVIM_TUI_ENABLE_CURSOR_SHAPE=0
" Nvim 0.2+から無効
set guicursor=

" --
" 基本設定
set title
" titleを表示
"
set lazyredraw
" terminal上でスクロールが遅くなるのを回避

set pumheight=10
" 補完ポップアップの高さ

set ignorecase
" 大文字と小文字を区別しない

set smartcase
" 大文字で検索したときは区別

set noincsearch
" インクリメンタルサーチを無効(Enterを押すまで探し始めない)

set nowrap
" 折り返さない

set scrolloff=5
" スクロール時に最低上下5行は表示

set number
" 行数表示

set showmatch
" 対応カッコを強調表示

set matchtime=1
" 対応カッコの表示時間は1s

set list listchars=tab:>-
" 不可視文字を表示

"set clipboard+=unnamedplus
" クリップボード有効化 (外部コマンドxclip/xselが必要, Macならpbcopy/pbpaste)
" ssh越しだと使えない

let g:tex_conceal = ''
" texハイライト示表をoff (https://github.com/vim-jp/issues/issues/529)

" --
" 日本語用の設定
setlocal formatoptions+=mM
" 連結時に空白を入れない

set spelllang=en,cjk
" 日本語はスペルチェックしない

set ambiwidth=double
" ○等のマルチバイト文字の表示くずれ防止
" (うまくいかない)

" --
" indent & tab
set autoindent
" 改行時に前のインデントを継続する

set expandtab
" tabは空白に変換

set smarttab
" shiftwidthを有効化

set ts=2
" [tabstop]

set sw=2
" [shiftwidth]

set sts=2
" [softtabstop]

" --
" shortcuts
tmap <silent> <esc> <c-\><c-n>
" Escでterminal mode(nvimで追加)を抜ける

nmap <esc><esc> :noh<cr>
" esc2回でハイライトoff

nmap <F9> :set spell<cr>
" F9でスペルチェックon
"
nmap <F10> :set nospell<cr>
" F10でスペルチェックoff

" --
" autocommand
augroup my_group
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") |
                   \   exe "normal! g`\"" |
                   \ endif
  "カーソルの位置を最後にカーソルがあった位置まで移動

  "au WinLeave *         set nocursorline
  "au WinEnter,BufRead * set cursorline
  "au WinLeave *         set nocursorcolumn
  "au WinEnter,BufRead * set cursorcolumn
  " 現在位置にカーソルを引く

  au FileType python set ts=8 sw=4 sts=4
  au FileType python set colorcolumn=80
  " 80行目に縦線を表示

  " tex
  au BufRead,BufNewFile *.tex set wrap
  au BufRead,BufNewFile *.tex set spell
augroup END
