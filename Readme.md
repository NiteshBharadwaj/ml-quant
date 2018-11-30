# Neural net to match volatility against Stochastic and Local Vol Models

Two loss functions:
	i) To have the output close to a known model (full computation graph is known)
	ii) To match SLV model (we don't know computation graph but neural net will find it eventually, hopefully)
The first loss is our prior. This can be from the current state-of-the art known to us. The second loss tries to move our model towards the unknown model. First, we train with loss 1 to learn the prior compute graph. Then, with a lower learning rate loss 2 is used online.

In all the experiments, known model is Black Cubic while unknown model is Dupire LV/Heston SLV. But the code can be used for any prior/posterior. 

Input is a coarse 2D grid of vol along strike and time (liquid instruments), while output is i) a much finer grid (calibrated vol surface) ii) a single point vol

### Experiment 0 - Creating vol surface (ground-truth creation):
[Quantlib](https://www.quantlib.org/) and it's [python hook](https://pypi.org/project/QuantLib-Python/) is used for vol surface calculations. For Heston, vol is interpolated on liquid instruments on time axis and then these pseudo-liquid instruments are used for calibration. For local vol, black cubic is used as the underlying implied vol surface and dupire formula on the implied vols and it's derivatives is directly used. Black Cubic is a bicubic interpolation along strike and maturity axis. Sticky Strike is the convention followed throughout. This [tutorial](http://gouthamanbalaraman.com/blog/volatility-smile-heston-model-calibration-quantlib-python.html) is the starting point for Heston using quantlib-python. Note: We are simulating Dupire/Heston as unknown. Ideally, we obtain ground-truth data from a source application.

To test the vol models, run the following command. It will generate visualizations in ../exp/ directory:
```
python volmodel_test.py -data ..\data\vol_raw_data.csv -expID testVolModel
```
![Vol Surface Img](vol_predictor/exp/testVolModel/vol_surface.png?raw=true "Vol Surfaces")
Ground truth is created by shifting the input vols and recalibrating the surfaces. Bivariate normal pdf with mean and correlation chosen uniformly randomly is added to input vols.
Figure below shows samples from the created data after calibration.
```
python volmodel_create_gt.py -data ..\data\vol_raw_data.csv -volModel black_cubic
```
![Ground truth data](vol_predictor/exp/augment_vol/augment_vol_samples.png?raw=true "GT Created")
 
### Experiment 1 - Learning the prior:
Model is trained with full supervision on known model. 
After 25 epochs, avg error in vol prediction (on test set) is 0.291% (gt vol range is 25% to 40%) 
```
python nnmodel_basic.py -expID base_model -data ..\data\black_cubic_annot.h5 -train
```
![Predicted_Vol_Surface](vol_predictor/exp/base_model_surface/base_model_surface.png?raw=true "Predicted Vol Surfaces")
  
### Experiment 2 - Learning the posterior:
For various percentages of available calibrated vols from the unknown model, model behavior is shown as gif.



To install dependencies:
```
pip install requirements.txt
```

To test:
i) Download trained models from _ and place in models folder.
ii) Place raw market quotes in /data/ folder

Run the following commands:
```
```
To train:

Data Preparation:
Sample data is in /data/ folder. Replace it with your data in the same format. It requires access to reuters. You can also replace processed data files in order to change the prior and posterior. 

Run this command to train:
```
```


