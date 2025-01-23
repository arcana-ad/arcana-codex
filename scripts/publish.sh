machine_type=$(uname -s)

if [ "$machine_type" = "Darwin" ]
then
    export $(grep -v '^#' .env | tr '\n' '\0' | xargs -0)
else
    export $(grep -v '^#' .env | xargs -d '\n')
fi


while getopts i: flag
do
    case "${flag}" in
        i) index=${OPTARG};;
    esac
done

if [ "$index" = "test" ]
then
    uv publish --index testpypi --username $TEST_PYPI_TOKEN_USERNAME --password $TEST_PYPI_TOKEN_PASSWORD
else
    uv publish --username $PYPI_TOKEN_USERNAME --password $PYPI_TOKEN_PASSWORD
fi
