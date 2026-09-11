# bash completion for batch-convert.sh
# Install to /etc/bash_completion.d/ or ~/.bash_completion.d/

_batch_convert() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    opts="-t --type -q --quiet -v --verbose -h --help --version"
    
    case "${prev}" in
        -t|--type)
            COMPREPLY=($(compgen -W "png jpg" -- "${cur}"))
            return 0
            ;;
        -q|--quiet|-v|--verbose|-h|--help|--version)
            return 0
            ;;
    esac
    
    if [[ ${cur} == -* ]]; then
        COMPREPLY=($(compgen -W "${opts}" -- "${cur}"))
        return 0
    fi
}

complete -F _batch_convert batch-convert.sh

