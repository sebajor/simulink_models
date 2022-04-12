% eigen_test/XSG_core_config
eigen_test_XSG_core_config_type         = 'xps_xsg';
eigen_test_XSG_core_config_param        = '';

% eigen_test/done
eigen_test_done_type         = 'xps_sw_reg';
eigen_test_done_param        = 'out';
eigen_test_done_ip_name      = 'opb_register_simulink2ppc';
eigen_test_done_addr_start   = hex2dec('01000000');
eigen_test_done_addr_end     = hex2dec('010000FF');

% eigen_test/dout
eigen_test_dout_type         = 'xps_bram';
eigen_test_dout_param        = '2048';
eigen_test_dout_ip_name      = 'bram_if';
eigen_test_dout_addr_start   = hex2dec('01002000');
eigen_test_dout_addr_end     = hex2dec('01003FFF');

% eigen_test/en
eigen_test_en_type         = 'xps_sw_reg';
eigen_test_en_param        = 'in';
eigen_test_en_ip_name      = 'opb_register_ppc2simulink';
eigen_test_en_addr_start   = hex2dec('01004000');
eigen_test_en_addr_end     = hex2dec('010040FF');

% eigen_test/read_size
eigen_test_read_size_type         = 'xps_sw_reg';
eigen_test_read_size_param        = 'in';
eigen_test_read_size_ip_name      = 'opb_register_ppc2simulink';
eigen_test_read_size_addr_start   = hex2dec('01004100');
eigen_test_read_size_addr_end     = hex2dec('010041FF');

% eigen_test/rst
eigen_test_rst_type         = 'xps_sw_reg';
eigen_test_rst_param        = 'in';
eigen_test_rst_ip_name      = 'opb_register_ppc2simulink';
eigen_test_rst_addr_start   = hex2dec('01004200');
eigen_test_rst_addr_end     = hex2dec('010042FF');

% eigen_test/seed
eigen_test_seed_type         = 'xps_sw_reg';
eigen_test_seed_param        = 'in';
eigen_test_seed_ip_name      = 'opb_register_ppc2simulink';
eigen_test_seed_addr_start   = hex2dec('01004300');
eigen_test_seed_addr_end     = hex2dec('010043FF');

