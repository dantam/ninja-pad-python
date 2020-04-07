# Python library for NinjaPad
## A private location tracker for contact tracing.

What contact tracers would ninjas use? What if they worked for different shoguns?

## For design, please see:
https://github.com/dantam/DataRocks/blob/master/Private%20Location%20Tracker.ipynb

## For round trip demo, please see:
https://github.com/dantam/ninja-pad-python/blob/master/src/jupyter/Plot%20Movement.ipynb

## To run independent processes:
```
% virtualenv --python=python3 venv
% source venv/bin/activate
% pip install -r requirements
% cd src
% export PYTHONPATH=.:$PYTHONPATH
% python demo/driver.py --steps c,s --one_time_pad_length=64 --key_size=2048 --num_users 10
% python bin/make_user_locations.py  --num_days 1 --num_users 10
% cat /tmp/user_locations.txt | python bin/process_user_locations.py --num_users 10
% python bin/run_medical_auth.py --patient_user_id 0 --num_users 10
% python bin/run_location_auth.py --num_users 10
% python bin/run_user_check_notification.py --num_users 10 --days_from_start 0
```
