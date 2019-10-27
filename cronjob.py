from crontab import Crontab

my_cron = Crontab(user='pi')
job = my_cron.new(command='python /home/pi/main.py >> /home/pi/output.txt 2>&1')
job.minute.every(1)

job.enable()
job.is_enabled()
my_cron.write()
