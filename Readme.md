# Neural net to match volatility against Stochastic and Local Vol Models

Two loss functions:
	i) To have the output close to a known model (full computation graph is known)
	ii) To match SLV model (we don't know computation graph but neural net will find it eventually, hopefully)
The first loss is our prior. This can be from the current state-of-the art known to us. The second loss tries to move our model towards the unknown model. First, we train with loss 1 to learn the prior compute graph. Then, with a lower learning rate loss 2 is used online.

In all the experiments, known model is Black Cubic while unknown model is Dupire LV/Heston SLV. But the code can be used for any prior/posterior. 

Input is a coarse 2D grid of vol along strike and time (liquid instruments), while output is i) a much finer grid (calibrated vol surface) ii) a single point vol

### Experiment 0 - Creating vol surface (ground-truth creation):
[Quantlib](https://www.quantlib.org/) and it's [python hook](https://pypi.org/project/QuantLib-Python/) are used for vol surface calculations. For Heston, vol is interpolated on liquid instruments along time axis and then these pseudo-liquid instruments are used for calibration. Once calibrated, black vols are implied from Heston prices. For local vol, black cubic is used as the underlying implied vol surface and dupire formula on the implied vols and it's derivatives is directly used. Black Cubic is a bicubic interpolation along strike and maturity axis. This [tutorial](http://gouthamanbalaraman.com/blog/volatility-smile-heston-model-calibration-quantlib-python.html) is the starting point for Heston using quantlib-python. Note: We are simulating Dupire/Heston as unknown. Ideally, we obtain ground-truth data from an upstream application.

To test the vol models, run the following command. It will generate visualizations in ../exp/ directory:
```
python volmodel_test.py -data ..\data\vol_raw_data.csv -expID testVolModel
```
![Vol Surface Img](vol_predictor/exp/testVolModel/vol_surface.png?raw=true "Vol Surfaces")
Ground truth is created by shifting the input vols and recalibrating the surfaces. Bivariate normal pdf with mean and correlation chosen uniformly randomly is added to input vols.
Figure below shows samples from the created data post calibration.
```
python volmodel_create_gt.py -data ..\data\vol_raw_data.csv -volModel black_cubic
```
![Ground truth data](vol_predictor/exp/augment_vol/augment_vol_samples.png?raw=true "GT Created")
 
### Experiment 1 - Learning the prior:
NN Model is trained with full supervision on known model. 
After 25 epochs, avg error in vol prediction (on test set) is 0.291% 
```
python nnmodel_basic.py -expID base_model -data ..\data\black_cubic_annot.h5 -train
```
![Predicted Black Cubic](vol_predictor/exp/base_model_surface/base_model_surface.png?raw=true "Predicted Black Cubic")
  
### Experiment 2 - Learning the posterior:
NN Model is trained on 5% of data with weights pre-initialized to predict prior. Avg Error in vol prediction is 3.89% for Heston (on test set) and 4.09% for Dupire (on test set).  
Dupire NN Prediction:
![Predicted Dupire Local](vol_predictor/exp/finetuneLocal/local_surface.png?raw=true "Predicted Dupire Local")
Heston NN Prediction:
![Predicted Heston SLV](vol_predictor/exp/finetuneSLV/slv_surface.png?raw=true "Predicted Heston SLV")

