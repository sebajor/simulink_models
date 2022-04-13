% test/XSG_core_config
test_XSG_core_config_type         = 'xps_xsg';
test_XSG_core_config_param        = '';

% test/gpio
test_gpio_type         = 'xps_gpio';
test_gpio_param        = '';
test_gpio_ip_name      = 'gpio_simulink2ext';

% test/gpio1
test_gpio1_type         = 'xps_gpio';
test_gpio1_param        = '';
test_gpio1_ip_name      = 'gpio_simulink2ext';

% test/gpio2
test_gpio2_type         = 'xps_gpio';
test_gpio2_param        = '';
test_gpio2_ip_name      = 'gpio_simulink2ext';

% test/gpio3
test_gpio3_type         = 'xps_gpio';
test_gpio3_param        = '';
test_gpio3_ip_name      = 'gpio_simulink2ext';

% test/gpio4
test_gpio4_type         = 'xps_gpio';
test_gpio4_param        = '';
test_gpio4_ip_name      = 'gpio_simulink2ext';

% test/gpio5
test_gpio5_type         = 'xps_gpio';
test_gpio5_param        = '';
test_gpio5_ip_name      = 'gpio_simulink2ext';

% test/gpio6
test_gpio6_type         = 'xps_gpio';
test_gpio6_param        = '';
test_gpio6_ip_name      = 'gpio_simulink2ext';

% test/gpio7
test_gpio7_type         = 'xps_gpio';
test_gpio7_param        = '';
test_gpio7_ip_name      = 'gpio_simulink2ext';

% test/in
test_in_type         = 'xps_sw_reg';
test_in_param        = 'in';
test_in_ip_name      = 'opb_register_ppc2simulink';
test_in_addr_start   = hex2dec('01000000');
test_in_addr_end     = hex2dec('010000FF');

% test/led
test_led_type         = 'xps_sw_reg';
test_led_param        = 'in';
test_led_ip_name      = 'opb_register_ppc2simulink';
test_led_addr_start   = hex2dec('01000100');
test_led_addr_end     = hex2dec('010001FF');

% test/out
test_out_type         = 'xps_sw_reg';
test_out_param        = 'out';
test_out_ip_name      = 'opb_register_simulink2ppc';
test_out_addr_start   = hex2dec('01000200');
test_out_addr_end     = hex2dec('010002FF');

