echo "BUILD CONTAINERS"
sudo docker-compose build
echo "APPLY MIGRATIONS"
sudo docker-compose run web bash -c "python block.py && ./manage.py migrate"
echo "COLLECT STATIC FILES"
sudo docker-compose run web ./manage.py collectstatic --noinput
echo "DONE"
