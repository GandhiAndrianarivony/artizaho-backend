export DJANGO_SETTINGS_MODULE=api.settings.base

# Basic configuration
PORT=8000

declare -A DOTENV_PATH
declare -A COMPOSE_FILE
declare -A DB_HOST_NAME
DOTENV_PATH=(["develop"]="dev.env" ["production"]="prod.env" ["staging"]="staging.env")
COMPOSE_FILE=(["develop"]="docker-compose-dev.yml" ["production"]="docker-compose-prod.yml" ["staging"]="docker-compose-staging.yml")
DB_HOST_NAME=(["develop"]="db-artizaho-dev" ["production"]="db-artizaho-prod" ["staging"]="db-artizaho-staging")



function run_migration() {
    echo '[INFO] Running migration ...'
    python3 manage.py makemigrations
    python3 manage.py migrate
    echo
}


function create_superuser() {
    echo '[INFO] Creating superuser ...'
    python3 manage.py createsuperuser --account_type E --noinput
    echo
}


function run_server() {
    python3 manage.py runserver "127.0.0.1:$1"

}


function load_db_config() {
    if [[ -f $1 ]]; then
        source $1
        export DJANGO_SUPERUSER_EMAIL="$DJANGO_SUPERUSER_EMAIL"
        export DJANGO_SUPERUSER_PASSWORD="$DJANGO_SUPERUSER_PASSWORD"
        export POSTGRES_USER="$POSTGRES_USER"
        export POSTGRES_PASSWORD="$POSTGRES_PASSWORD"
        export POSTGRES_DB="$POSTGRES_DB"
        export DB_HOST="127.0.0.1"
        export DB_PORT="5732" 
        export SECRET_KEY="$SECRET_KEY"
        return 0
    else
        return 1
    fi
}


function run_db() {
    echo '[INFO] Run Application DB ...'
    echo
    docker-compose -f $1 up $2 -d
}


function down_db() {
    docker-compose -f $1 down $2
}


# CHOOSE ENVIRONMENT
echo '[INFO] Load database configuration ...'
read -p "Choose environment: [1)dev 2)prod 3)staging]: " env
case $env in 
    1) 
        compose_file="${COMPOSE_FILE[develop]}" 
        dotenv_path="${DOTENV_PATH[develop]}"
        db_host_name="${DB_HOST_NAME[develop]}"
        ;;
    2)
        compose_file="${COMPOSE_FILE[production]}" 
        dotenv_path="${DOTENV_PATH[production]}"
        db_host_name="${DB_HOST_NAME[production]}"
        ;;
    3)
        compose_file="${COMPOSE_FILE[staging]}" 
        dotenv_path="${DOTENV_PATH[staging]}"
        db_host_name="${DB_HOST_NAME[production]}"
        ;;
    *) 
        echo "Unknown command"
        exit 1
        ;;
esac


# RUN DATABASE
load_db_config "$dotenv_path" 
is_loaded=$?
if [[ $is_loaded == 0 ]]; then
    echo "[INFO] Environment variables from $dotenv_path loaded"
    echo
else
    echo "[ERROR MESSAGE] File ($dotenv_path) not found"
    echo
    exit 1
fi
run_db "$compose_file" "$db_host_name"


read -p "Want to run migration: [y/n]? " res
if [[ $res == 'y' ]]; then
    run_migration
fi

read -p "Want to create superuser: [y/n]? " res
if [[ $res == 'y' ]]; then
    create_superuser
fi


# RUN SERVER
python3 manage.py spectacular --file schema.yml

run_server "$PORT"
down_db "$compose_file" "$db_host_name"
