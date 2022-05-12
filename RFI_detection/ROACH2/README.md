# RFI detection

This system is based in [this thesis](http://www.das.uchile.cl/lab_mwl/publicaciones/Tesis/RFI-detection-Engineer_thesis-Daniel_Bravo.pdf) but in this implementation we want to use only the strictly necessary resources. So for example we reduce the bitwidths and use them



The parameters used in the sample model are meant to work with the ARTE receiver and the bitwidths are selected to operate in the pass band of that receiver.
For the selection of the parameters we collected data from the enviroment, and then use that data as input for a simulation which to find the necessary bitwidths.
Tests in the laboratory shows that the system in the model folder will detect RFI in the power range (-16dBm, -41dBm).
