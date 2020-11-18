" initialize
if &compatible
  set nocompatible
endif

let s:dein_dir = expand('<sfile>:p:h')
let s:dein_repo_dir = s:dein_dir.'/repos/github.com/Shougo/dein.vim'

" install if not exists
if !isdirectory(s:dein_repo_dir)
  call system('git clone https://github.com/Shougo/dein.vim '.s:dein_repo_dir)
endif

" add runtimepath
let &runtimepath = &runtimepath.",".s:dein_repo_dir

" load python_host
if filereadable(expand('<sfile>:p:h').'/python.vim')
  source <sfile>:p:h/python.vim
endif

" plugin manger
if dein#load_state(s:dein_dir)
  call dein#begin(s:dein_dir)

  call dein#load_toml(s:dein_dir.'/dein.toml')
  call dein#load_toml(s:dein_dir.'/python.toml')

  call dein#end()
  call dein#save_state()
endif

" install missing plugins
if dein#check_install()
  call dein#install()
endif
