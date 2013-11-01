/* to compile this, your MIKENET_DIR environment variable
   must be set to the appropriate directory.  putting this
   at the bottom of your .cshrc file will do the trick:

   setenv MIKENET_DIR ~mharm/mikenet/default/
   */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#ifdef unix
#include <unistd.h>
#endif

#include <mikenet/simulator.h>

#define TIME 3
unsigned int REP = 1000;
unsigned int ITER = 10000;
unsigned int VERBOSE=0;
int main(int argc,const char *argv[])
{
  Net *net;
  Group *input,*hidden,*output,*bias;
  ExampleSet *examples, *test;
  Example *ex;
  Connections *c1,*c2,*c3,*c4;
  char * fileName = "input";
  int i,count,j, dataCount =0, testCount = 0;
  int dataCountArray[6] = {0};
  char * testFileArray[6] = {NULL};
  int inputCount = 0,outputCount = 0, hiddenCount = 200;
  int batchFlag = 0;
  Real error, correct;
  Real epsilon,range, hiddenRatio = 0;
  unsigned long seed = 0;
  /* don't buffer output */
  setbuf(stdout,NULL);

  /* set seed to unique number */
  mikenet_set_seed(seed);

  /* a default learning rate */
  epsilon=0.1;

  /* default weight range */
  range=0.5;

  default_errorRadius=0.0;
  const char *usage = "mike_childes [options]\n"
    "-seed\t\tRandom seed (default to 0)\n"
    "-i\t\tNumer of input units (default to 0)\n"
    "-h\t\tNumer of hidden units (default to 200)\n"
    "-o\t\tNumer of output units (default to 0)\n"
    "-r\t\tRatio of input units / hidden units.(default to 200)\n"
    "-b\t\tEnables batch learning (default online learning)\n"
    "-epsilon\tBack probagation epsilon (Default 0.1)\n"
    "-help\t\tprints this help\n";
  /* what are the command line arguments? */
  if (argc == 1) {
    fprintf(stderr, "%s", usage);
    exit(1);
  }
  for(i=1;i<argc;i++) {
    if (strcmp(argv[i],"-seed")==0) {
      seed = atol(argv[i+1]);
      mikenet_set_seed(seed);
      i++;
    } else if (strncmp(argv[i],"-epsilon",5)==0) {
      epsilon=atof(argv[i+1]);
      i++;
    } else if (strcmp(argv[i],"-range")==0) {
      range=atof(argv[i+1]);
      i++;
    } else if (strcmp(argv[i],"-errorRadius")==0) {
      default_errorRadius=atof(argv[i+1]);
      i++;
    } else if (strcmp(argv[i],"-t")==0){
      testFileArray[testCount] = (char *)argv[i+1];
      testCount++;
      i++;
    } else if (strcmp(argv[i],"-d")==0){
      dataCountArray[dataCount]= atoi(argv[i+1]);
      dataCount++;
      i++;
    } else if (strcmp(argv[i], "-iter")==0) {
      ITER = atoi(argv[i+1]);
      i++;
    } else if (strcmp(argv[i], "-f") == 0) {
      fileName = (char*)argv[i+1];
      i++;
    } else if (strcmp(argv[i], "-v") == 0) {
      VERBOSE = 1;
    } else if (strcmp(argv[i], "-i") == 0) {
      inputCount = atoi(argv[i+1]);
      i++;
    } else if (strcmp(argv[i], "-o") == 0) {
      outputCount = atoi(argv[i+1]);
      i++;
    } else if (strcmp(argv[i], "-h") == 0) {
      hiddenCount = atoi(argv[i+1]);
      i++;
    } else if (strcmp(argv[i], "-r") == 0) {
      hiddenRatio = atof(argv[i+1]);
      i++;
    } else if (strcmp(argv[i], "-b") == 0) {
      batchFlag = 1;
    } else {
      fprintf(stderr,"unknown argument: %s\n%s\n",argv[i],usage);
      exit(-1);
    }
  }

  /* build a network, with TIME number of time ticks */
  net=create_net(TIME);

  /* learning rate */
  default_epsilon=epsilon;

  /* hidden ratio */
  if (hiddenRatio > 0 && hiddenRatio <= 1) {
    hiddenCount = (int)inputCount * hiddenRatio;
    if(VERBOSE) fprintf(stderr, "number of hidden units is set to %d\n",hiddenCount);
  } else if(hiddenRatio > 1) {
    fprintf(stderr, "%s", usage);
    exit(1);
  }
  /* First stdout of this code is nummber of hidden units*/
  printf("%d\t",hiddenCount);
  /* create our groups.  
     format is: name, num of units, ticks */

  input=init_group("Input",inputCount,TIME);
  hidden=init_group("hidden",hiddenCount,TIME);
  output=init_group("Output",outputCount,TIME);

  /* bias is special.  format is: value, ticks */
  bias=init_bias(1.0,TIME);   

  /* now add our groups to the network object */
  bind_group_to_net(net,input);
  bind_group_to_net(net,hidden);
  bind_group_to_net(net,output);
  bind_group_to_net(net,bias);

  /* now connect our groups, instantiating */
  /* connection objects c1 through c4 */
  c1=connect_groups(input,hidden);
  c2=connect_groups(hidden,output);
  c3=connect_groups(bias,hidden);
  c4=connect_groups(bias,output);

  /* add connections to our network */
  bind_connection_to_net(net,c1);
  bind_connection_to_net(net,c2);
  bind_connection_to_net(net,c3);
  bind_connection_to_net(net,c4);

  /* randomize the weights in the connection objects.
     2nd argument is weight range. */
  randomize_connections(c1,range);
  randomize_connections(c2,range);
  randomize_connections(c3,range);
  randomize_connections(c4,range);

  /* how to load and save weights */
  /*  load_weights(net,"init.weights");   */

  /* erase old initial weight file */
  /*  system("rm -f init.weights.Z");      */

  /* save out our weights to file 'init.weights' */

  /* load in our example set */
  if (VERBOSE){
    fprintf(stderr, "Reading %s Iter:%d ",fileName, ITER);
    for(i=0; i < 6; i++){
      if (testFileArray[i] == NULL) break;
      fprintf(stderr, "TestSet:%s\n", testFileArray[i]);               
    }
  }
  examples=load_examples(fileName,TIME);
  if (VERBOSE){
    fprintf(stderr, "size:%d\n", examples->numExamples);     
    for(i=0; i < dataCount; i++){
      if (i == 0){
        fprintf(stderr, "DataCounts[%d] start:0 end:%d size:%d\n", \
            i,dataCountArray[i],dataCountArray[i]);
      }else{
        fprintf(stderr, "DataCounts[%d] start:%d end:%d size:%d\n", \
            i,dataCountArray[i - 1], dataCountArray[i], dataCountArray[i] - dataCountArray[i - 1]);
      }
    }
  }
  error=0.0;
  count=0;
  /* loop for ITER number of times */
  /* Reset the seed to get same training set*/
  fprintf(stderr, "Training: %s size:%d\n", fileName, examples->numExamples);     
  mikenet_set_seed(seed);     
  for(i=0;i<ITER;i++) {
    /* get j'th example from exampleset */
    int ridx = (int) (mikenet_random() * (Real)examples->numExamples);
    ex = &examples->examples[ridx];
    /*Original one*/
    // ex = get_random_example(examples);
    
    /* do forward propagation */
    bptt_forward(net,ex);

    /* backward pass: compute gradients */
    bptt_compute_gradients(net,ex);

    /* sum up error for this example */
    error+=compute_error(net,ex);

    /* online learning: apply the deltas 
       from previous call to compute_gradients */
    if(batchFlag == 0)  
      bptt_apply_deltas(net);

    /* is it time to write status? */
    if (count==REP) {
      /* average error over last 'count' iterations */
      error = error/(float)count;
      count=0;

      /* print a message about average error so far */
      if (VERBOSE) fprintf(stderr, "%d\t%f\n",i,error);
      if (error < 0.1) {
        break;
      }
      /* zero error; start counting again */
      error=0.0;
    }
    count++;
  }
  if(batchFlag == 1) 
      bptt_apply_deltas(net);
  /* done training.  write out results for each example */
  if (testCount == 0){
    correct = 0;
    dataCount = 0;
    for(i=0;i<examples->numExamples;i++)
    {
      if (VERBOSE && i % 1000 == 0) fprintf(stderr,".");
      if (dataCount && i == dataCountArray[dataCount]){
        if (dataCount ==0){
          printf("%f\t", correct / dataCountArray[dataCount]);
        }else{
          printf("%f\t", correct / (dataCountArray[dataCount] - dataCountArray[dataCount - 1]));

        }
        correct = 0;
        dataCount++;
      }
      ex=&examples->examples[i];
      bptt_forward(net,ex);
      int maxj = -1;
      Real  maxx = 0;
      for(j=0 ; j < outputCount; j++){
        if (output->outputs[TIME-1][j] > maxx){
          maxj = j;
          maxx = output->outputs[TIME-1][j];
        }
        /* printf("%d:%f ",j,output->outputs[TIME-1][j]); */
      }
      if (get_value(ex->targets,output->index,TIME-1,maxj) == 1)
        correct += 1;
    }
    printf("%f\n", correct / (dataCountArray[dataCount] - dataCountArray[dataCount - 1]));
  }
  else{
    int tt = 0, dc = 0;
    correct = 0;
    for(tt = 0; tt < testCount; tt++){
      test = load_examples(testFileArray[tt],TIME);
      if (VERBOSE)
        fprintf(stderr,"Testing:%s size:%d\n",testFileArray[tt],test->numExamples);
      correct = 0;
      for(i=0;i<test->numExamples;i++){
        if (dataCount && i == dataCountArray[dc]){
          if (dc == 0)
            printf("%f\t", correct / dataCountArray[dc]);
          else
            printf("%f\t", correct / (dataCountArray[dc] - dataCountArray[dc - 1]));                         
          correct = 0;
          dc++;
        }
        if (VERBOSE && i % 1000 == 0) fprintf(stderr,".");
        ex=&test->examples[i];
        bptt_forward(net,ex);
        int maxj = -1;
        Real  maxx = 0;
        int goldIdx = -1; 
        for(j=0 ; j < outputCount; j++){
          if (output->outputs[TIME-1][j] > maxx){
            maxj = j;
            maxx = output->outputs[TIME-1][j];
          } 
          if (get_value(ex->targets,output->index,TIME-1,j) == 1) {
            if(goldIdx != -1) {
              fprintf(stderr,\
                  "Multiple active output unit: Instance:%d unit:%d in test set!"\
                  ,i,j);
            }
            goldIdx = j; 
          }
          /* printf("%d:%f ",j,output->outputs[TIME-1][j]); */
        }
        if (goldIdx != -1 || maxj != -1) {
          // prints the goldtag and answer tag
          fprintf(stderr, "%d %d\n", goldIdx, maxj);
        } else{
          fprintf(stderr, "No active output units in test set");
          exit(-1);
        }
        if (get_value(ex->targets,output->index,TIME-1,maxj) == 1) {
          correct += 1;
        }
      }
      if (dataCount == 0)
        printf("%f %d %d\t", correct / test->numExamples, (int)correct, test->numExamples);
      else
        printf("%f\n", correct / (dataCountArray[dc] - dataCountArray[dc - 1]));
    }
  }
  return 0;
}
