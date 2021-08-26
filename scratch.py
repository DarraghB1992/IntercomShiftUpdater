if admin_start_hour > admin_finish_hour:
    current_day = dt.datetime.now().day
    current_unix_timestamp = time.time()
    tomorrow_day = current_day + 1
    start_date = dt.datetime.now().strftime('%d/%m/%Y %' + str(admin_start_hour) + ':%M:%S')
    end_date = dt.datetime.now().strftime(str(tomorrow_day) + '/%m/%Y %' + str(admin_start_hour) + ':%M:%S')
    start_time_in_unix = dt.datetime.strptime(start_date, '%d/%m/%Y %H:%M:%S').timestamp()
    end_time_in_unix = dt.datetime.strptime(end_date, '%d/%m/%Y %H:%M:%S').timestamp()
    if current_unix_timestamp in range(int(start_time_in_unix), int(end_time_in_unix)):
        print('In here')
        print(str(start_time_in_unix), str(end_time_in_unix))
        set_admin_as_online(admin_id)
    else:
        set_admin_as_away(admin_id)