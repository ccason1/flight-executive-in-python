import fexecutive as fe
import time
import math
import csv
        

def setup_telemetry_points():

    telemetry_points = []
        
    def get_acc_data():
        #time.sleep(1)
        return ['acc']
    
    acc = fe.TelemetryPoint(name='acc', min_time_interval=2, data_getter=get_acc_data, header='acc')
    telemetry_points.append(acc)
    
    def get_tmp_data():
        #time.sleep(1)
        return ['tmp', 'col2', 'col3']
    
    tmp = fe.TelemetryPoint(name='tmp', min_time_interval=5, data_getter=get_tmp_data, header='tmp')
    telemetry_points.append(tmp)
    
    def get_env_data():
        #time.sleep(3)
        return ['env', 'col2']
    
    env = fe.TelemetryPoint(name='env', min_time_interval=8, data_getter=get_env_data, header='env')
    telemetry_points.append(env)
    
    return telemetry_points


# def run_tests():
    
    #test minimum time between messages
    # if end_time - start_time >= rb_min_time_interval * max_messages:
        # print("Success: At least the minimum time passed between messages")
    # else:
        # print("Failed: Not enough time passed between messages")
    
    #test number of rockblock messages sent
    # rockblock.msg_count_file.seek(0)
    # number_of_messages_in_file = int(rockblock.msg_count_file.read())
    # number_of_messages_var = rockblock.msg_count
    # number_of_messages_sent = len(sent_messages)
    
    # if number_of_messages_in_file == number_of_messages_var and number_of_messages_var == number_of_messages_sent:
        # print("Success: The number of rockblock messages sent is consistent")
    # else:
        # print("Failed: The number of rockblock messages sent is inconsistent")
    
    #test data logs
    # acc.output_file.seek(0)
    # tmp.output_file.seek(0)
    
    # acc_lines = list(csv.reader(acc.output_file))
    # tmp_lines = list(csv.reader(tmp.output_file))
    
    # test_lines = [['col1', 'col2'] for _ in range(3)]
    
    # number_of_lines_to_test = 3
    
    # if [line[1:] for line in acc_lines][:number_of_lines_to_test] == test_lines[:number_of_lines_to_test] and \
            # [line[1:] for line in tmp_lines][:number_of_lines_to_test] == test_lines[:number_of_lines_to_test]:
        # print("Success: Data logging correctly")
    # else:
        # print("Failed: Data logging incorrectly")
    
    #close files
    # for point in telemetry_points:
        # point.close_file()
    
    # rockblock.close_file()


def log(telemetry_point):
    
    # when enough time has passed, update the message and log
    if telemetry_point.is_ready_to_update():
        
        # call the telemetry point's data getter function to retrieve the latest input data
        telemetry_point.update()
        
        telemetry_point.log_to_csv()


# flight loop
def main_execution_loop(telemetry_points, rockblock):
    
    for point in telemetry_points:
        log(point)
    
    if rockblock.is_ready_to_send():
        rockblock_msg = ';'.join([','.join(p.data) for p in telemetry_points])
        
        rockblock.send(rockblock_msg)
    
    # to prevent unnecessary iterations that drain the battery
    time.sleep(0.1)


def main():
    
    telemetry_points = setup_telemetry_points()
    
    # do this on the first boot
    for pt in telemetry_points:
        pt.clear_file()
    
    rockblock = fe.Rockblock(min_time_interval=4, should_send=False)
    
    # do this on the first boot
    rockblock.reset_msg_count()
    
    while True:
        # execute the flight loop
        # set send_rockblock_data to False for testing
        main_execution_loop(telemetry_points, rockblock)
    
    for point in telemetry_points:
        point.close_file()
    
    rockblock.close_file()
    
    run_tests()


if __name__ == '__main__':
    main()