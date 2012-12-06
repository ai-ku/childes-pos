/*
Fast Artificial Neural Network Library (fann)
Copyright (C) 2003-2012 Steffen Nissen (sn@leenissen.dk)

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <stdio.h>

#include "fann.h"

int FANN_API test_callback(struct fann *ann, struct fann_train_data *train,
	unsigned int max_epochs, unsigned int epochs_between_reports, 
	float desired_error, unsigned int epochs)
{
	printf("Epochs     %8d. MSE: %.5f. Desired-MSE: %.5f\n", epochs, fann_get_MSE(ann), desired_error);
	return 0;
}

void shuffle(struct fann_train_data *train_data)
{
	unsigned int dat = 0, elem, swap;
	fann_type temp;
     srand(0);
	for(; dat < train_data->num_data; dat++)
	{
		swap = (unsigned int) (rand() % train_data->num_data);
		if(swap != dat)
		{
			for(elem = 0; elem < train_data->num_input; elem++)
			{
				temp = train_data->input[dat][elem];
				train_data->input[dat][elem] = train_data->input[swap][elem];
				train_data->input[swap][elem] = temp;
			}
			for(elem = 0; elem < train_data->num_output; elem++)
			{
				temp = train_data->output[dat][elem];
				train_data->output[dat][elem] = train_data->output[swap][elem];
				train_data->output[swap][elem] = temp;
			}
		}
	}
}

int main(int argc, const char ** argv)
{
	fann_type *calc_out;
	const unsigned int num_layers = 3;
	const unsigned int num_neurons_hidden = 200;
	const float desired_error = (const float) 0;
     const float learning_rate = 0.1;
	const unsigned int max_epochs = 1;
	const unsigned int epochs_between_reports = 1;
     unsigned  int subsize = 10000;
	struct fann *ann;
	struct fann_train_data *data, *tdata;

	unsigned int i = 0,j=0;
	unsigned int decimal_point;
     if (argc < 2){
          fprintf(stderr, "Missing input\n");
          exit(-1);
     }
     else if (argc == 3){
          subsize = atoi(argv[2]);
     }
	fprintf(stderr, "Reading network\n");
	data = fann_read_train_from_file(argv[1]);
     shuffle(data);
     if (fann_length_train_data(data) < subsize){
          fprintf(stderr,"sub-size decreased to %d from %d\n",fann_length_train_data(data),subsize);
          subsize = fann_length_train_data(data);
     }
     if (subsize > 0){
          fprintf(stderr, "Subsample to:%d\n",subsize);
          tdata = fann_subset_train_data(data,0,subsize);
     }
     else {
          fprintf(stderr, "All data epoch:%d\n",max_epochs);
          tdata = data;
     }
	fprintf(stderr, "Creating network.\n");
     fprintf(stderr, "Input:%d, Output:%d Instance:%d\n",\
          tdata->num_input, tdata->num_output,fann_length_train_data(data));
     
	ann = fann_create_standard(num_layers, tdata->num_input, num_neurons_hidden, tdata->num_output);
	fann_set_activation_steepness_hidden(ann, 1);
	fann_set_activation_steepness_output(ann, 1);
     
	fann_set_activation_function_hidden(ann, FANN_SIGMOID);
	fann_set_activation_function_output(ann, FANN_SIGMOID);
     fann_set_learning_rate(ann, learning_rate);
     /*	fann_set_train_stop_function(ann, FANN_STOPFUNC_BIT);*/
	/* fann_set_bit_fail_limit(ann, 0.01f);*/

	fann_set_training_algorithm(ann, FANN_TRAIN_INCREMENTAL);
     fann_randomize_weights(ann,-0.5,-0.5);
	/* fann_init_weights(ann, tdata); */
	
	fann_train_on_data(ann, tdata, max_epochs, epochs_between_reports, desired_error);
	fann_reset_MSE(ann);
     fprintf(stderr, "Testing network. %f\n", fann_test_data(ann, data));
     double sum = 0;
	for(i = 0; i < fann_length_train_data(data); i++)
	{
          float max = 0;
          int maxj = -1;
		calc_out = fann_test(ann, data->input[i], data->output[i]);
          for(j = 0 ; j < data-> num_output; j++){
               if (calc_out[j] > max) {
                    max = calc_out[j];
                    maxj = j;
               }
          }
          if (data->output[i][maxj] == 1) sum += 1;
          //          printf("%f %f\n",data->output[i][maxj],sum);
	}
     sum /= fann_length_train_data(data);
	fprintf(stderr,"MSE error on test data: %f maliy:%f\n", fann_get_MSE(ann), 1 - sum);
	fprintf(stdout,"MSE error on test data: %f maliy:%f\n", fann_get_MSE(ann), 1 - sum);
	fprintf(stderr,"Saving network.\n");

	fann_save(ann, "childes.net");

	decimal_point = fann_save_to_fixed(ann, "childes_fixed.net");
	fann_save_train_to_fixed(tdata, "childes_fixed.data", decimal_point);

	fprintf(stderr, "Cleaning up.\n");
	fann_destroy_train(data);
     if (data != tdata)
          fann_destroy_train(tdata);
	fann_destroy(ann);

	return 0;
}
