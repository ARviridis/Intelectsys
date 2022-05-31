# PATTERN_RECOGNITION

PyQt5,scipy,matplotlib,numpy

The method of clustering by k averages requires the number of clusters to be set to k. 
The first step in the feature space, the position of k centers of clusters is chosen arbitrarily, not necessarily coinciding with any images. 
Then at each step, first, each image belongs to that cluster, the distance to the center of which for it is minimal, and secondly, after all images have been distributed into clusters the position of the cluster centers is recalculated. 
The process continues until the the composition of the clusters is stabilized.


example:  
![til](./k_averages/assets/GIF.gif)  
  
  
The Kohonen layer works according to the "winner takes all" algorithm. For each neuron of the layer the excitation levelis calculated.
The neuron with the maximal value of s outputs one, all others output zero, forming vector Y. 
The process of learning, which is actually clustering of the given set of images, consists in changing weights of the "winning" neuron.
As a result of learning, different input vectors should activate different neurons, and similar ones - one and the same neuron, but it is not specified which neuron it is before the learning. 
Weights of the first neuron of the Kohonen layer are taken equal to normalized feature values of arbitrary image from the set of images set for clustering. Weights of the second neuron are equal to normalized feature values of the image that is at the maximal distance from the image, chosen to set weights of the first neuron. To set weights of the following neurons, we select the image that is at the maximal distance from the nearest image, already selected to set weights of the previous neurons. The distance between images in the feature space is Euclidean.  
  
   
example:    
![til](./kohonen_layer_with_neuron/assets/GIFkohen.gif)   
  