from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import Codes.sent_sim_edited as sse
import time
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = ''
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] ='MyFiles'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])

app.config["JSON_SORT_KEYS"] = False



@app.route("/recieveText", methods=['GET','POST'])
def recieveText():
  if(request.method == "POST"):
    plag_text= request.form['plag_text']
    file1 = open("Test_document.txt","w")
    file1.write(plag_text)
    file1.close()

    return jsonify({"status":"success"})
  else:
    return jsonify({"status":"failure"})



@app.route("/sent")
def home_page():

    # #Start the time
    start = time.time()

    UsersDocument="Test_document.txt"
    Perc, SentenceListOfUser, DocsPerc =sse.sent_sim_main(UsersDocument)
    finalJson = {}


    finalJson['perc']=int(Perc)
    finalJson['DocsPerc']=DocsPerc
    finalJson['userSentences']=SentenceListOfUser

    #End Time
    end = time.time()
    print("Execution time:",end-start)
    return jsonify(finalJson)


@app.route("/")
def helloWorld():
   return jsonify({'posts':'Hello World!'})

@app.route("/demo")
def demo():
  posts= {"perc": 40, "DocsPerc": {"https://arxiv.org/pdf/1711.11585v2.pdf": 13, "https://arxiv.org/pdf/1711.10275v1.pdf": 12, "https://arxiv.org/pdf/1502.03240v3.pdf": 7}, "userSentences": {"0": ["", "notplag", "none", "none"], "1": ["Generating Publicity about our Business:", "notplag", "none", "none"], "2": ["", "notplag", "none", "none"], "3": ["1.", "notplag", "none", "none"], "4": ["Write Positioning Statement  Sums up what makes your business different from the competition", "notplag", "none", "none"], "5": ["2.", "notplag", "none", "none"], "6": ["List your objectives  What do you hope to achieve for your company through the publicity plan you put into action?", "notplag", "none", "none"], "7": ["List your top five goals in order of priority.", "notplag", "none", "none"], "8": ["Be specific, and always set deadlines.", "notplag", "none", "none"], "9": ["Using a clothing boutique as an example, some goals may be to:", "notplag", "none", "none"], "10": ["a. increase your store traffic, which will translate into increased sales", "notplag", "none", "none"], "11": ["b. create a high profile for your store within the community", "notplag", "none", "none"], "12": ["3.", "notplag", "none", "none"], "13": ["Identify your target customers  Are they male or female?", "notplag", "none", "none"], "14": ["What is the age range?", "notplag", "none", "none"], "15": ["What are their lifestyle, income and buying habits?", "notplag", "none", "none"], "16": ["Where do they live?", "notplag", "none", "none"], "17": ["4.", "notplag", "none", "none"], "18": ["Identify your target media - List the newspapers and TV and radio programs in your area that would be appropriate outlets.", "notplag", "none", "none"], "19": ["Make a complete list of the media you want to target, then call them and ask whom you should contact regarding your area of business.", "notplag", "none", "none"], "20": ["Identify the specific reporter or producer who covers your area so you can contact them directly.", "notplag", "none", "none"], "21": ["Your local library will have media reference books that list contact names and numbers.", "notplag", "none", "none"], "22": ["Make your own media directory, listing names, addresses, and telephone numbers.", "notplag", "none", "none"], "23": ["Separate TV, radio and print sources.", "notplag", "none", "none"], "24": ["Know the \"beats\" covered by different reporters so you can be sure you are pitching your ideas to the appropriate person.", "notplag", "none", "none"], "25": ["5.", "notplag", "none", "none"], "26": ["In this section we provide a brief overview of Condi- tional Random Fields (CRF) for pixel-wise labelling and introduce the notation used in the paper.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "Conditional Random Fields In this section we provide a brief overview of Conditional Random Fields (CRF) for pixel-wise labelling and introduce the notation used in the paper."], "27": ["A CRF, used in the context of pixel-wise label prediction, models pixel la- bels as random variables that form a Markov Random Field (MRF) when conditioned upon a global observation.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "A CRF, used in the context of pixel-wise label prediction, models pixel labels as random variables that form a Markov Random Field (MRF) when conditioned upon a global observation."], "28": ["The global observation is usually taken to be the image.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "The global observation is usually taken to be the image."], "29": ["6.", "notplag", "none", "none"], "30": ["Minimizing the above CRF energy E(x) yields the most probable label assignment x for the given image.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "Minimizing the above CRF energy E(x) yields the most probable label assignment x for the given image."], "31": ["Since this exact minimization is intractable, a mean-field approxima- tion to the CRF distribution is used for approximate max- imum posterior marginal inference.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "Since this exact minimization is intractable, a mean-field approximation to the CRF distribution is used for approximate maximum posterior marginal inference."], "32": ["It consists in approxi- mating the CRF distribution P (X) by a simpler distribution Q(X), which can be written as the product of independent marginal distributions, i.e., Q(X) = i Qi(Xi).", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "It consists in approximating the CRF distribution P(X) by a simpler distribution Q(X), which can be written as the product of independent marginal distributions, i.e., Q(X) = Q i Qi(Xi)."], "33": ["The steps of the iterative algorithm for approximate mean-field infer- ence and its reformulation as an RNN are discussed next.", "plag", "https://arxiv.org/pdf/1502.03240v3.pdf", "The steps of the iterative algorithm for approximate mean-field inference and its reformulation as an RNN are discussed next."], "34": ["Convolutional networks are standard for an- alyzing spatio-temporal data such as images, videos, and 3D shapes.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "Convolutional networks are the de-facto standard for an- alyzing spatio-temporal data such as images, videos, and 3D shapes."], "35": ["Whilst some of this data is naturally dense (e.g., photos), many data sources are inherently sparse.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "Whilst some of this data is naturally dense (e.g., photos), many other data sources are inherently sparse."], "36": ["Examples include 3D point clouds that are obtained using a LiDAR scanner/RGB-D camera.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "Examples include 3D point clouds that were ob- tained using a LiDAR scanner or RGB-D camera."], "37": ["Standard dense implementations of convolutional networks are very inefficient when applied for such sparse data.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "Stan- dard \u201cdense\u201d implementations of convolutional networks are very inef\ufb01cient when applied on such sparse data."], "38": ["We introduce new sparse convolutional operations that are de- signed to process spatially-sparse data more efficiently, and use them for developing spatially-sparse convolutional networks.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "We introduce new sparse convolutional operations that are de- signed to process spatially-sparse data more ef\ufb01ciently, and use them to develop spatially-sparse convolutional networks."], "39": ["We demonstrate that this strong performance of the resulting models, called submanifold sparse convolutional networks (SSCNs), for two tasks involving semantic seg- mentation of 3D point clouds.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "We demonstrate the strong performance of the resulting models, called submanifold sparse convolutional networks (SSCNs), on two tasks involving semantic seg- mentation of 3D point clouds."], "40": ["In particular, the models outperform all prior state of the art on the test set of recent semantic segmentation competition.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "In particular, our models outperform all prior state-of-the-art on the test set of a re- cent semantic segmentation competition."], "41": ["Prior work on sparse convolutions implemented a convolutional operator that increased the number of active sites with each layer.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "Prior work on sparse convolutions implements a convo- lutional operator that increases the number of active sites with each layer [3, 4]."], "42": ["In, all sites that have at least one active input site are considered as active.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "In [4], all sites that have at least one \u201cactive\u201d input site are considered as active."], "43": ["In, a greater degree of sparsity is attained after the convolution has been calculated by using Relus and a special loss function.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "In [3], a greater degree of sparsity is attained after the convolution has been calculated by using ReLUs and a special loss In contrast, we introduce submanifold sparse function."], "44": ["In contrast, we introduce submanifold sparse convolutions that fix the location of active sites so that the sparsity remains unchanged for many layers.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "convolutions that \ufb01x the location of active sites so that the sparsity remains unchanged for many layers."], "45": ["We show that this makes it practical to train deep and efficient net- works similar to VGG networks or Resnets, and that it is well suited for the task of point-wise semantic segmentation.", "plag", "https://arxiv.org/pdf/1711.10275v1.pdf", "We show that this makes it practical to train deep and ef\ufb01cient net- works similar to VGG networks [20] or ResNets [7], and that it is well suited for the task of point-wise semantic segmentation."], "46": ["Photo-realistic image rendering using standard graphics techniques is involved, since geometry, materials, and light transport must be simulated explicitly.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "Photo-realistic image rendering using standard graphics techniques is involved, since geometry, materials, and light transport must be simulated explicitly."], "47": ["Although existing graphics algorithms excel at the task, building and editing virtual environments is expensive and time-consuming.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "Although existing graphics algorithms excel at the task, building and edit- ing virtual environments is expensive and time-consuming."], "48": ["That is because we have to model every aspect of the world explicitly.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "That is because we have to model every aspect of the world explicitly."], "49": ["If we were able to render photo-realistic images using a model learned from data, we could turn the process of graphics rendering into a model learning and inference problem.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "If we were able to render photo-realistic images using a model learned from data, we could turn the process of graphics rendering into a model learning and inference problem."], "50": ["Then, we could simplify the process of creating new virtual worlds by training models on new datasets.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "Then, we could simplify the process of creating new virtual worlds by training models on new datasets."], "51": ["We could even make it easier to customize environments by al- lowing users to simply specify overall semantic structure rather than modeling geometry, materials, or lighting.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "We could even make it easier to customize environments by al- lowing users to simply specify overall semantic structure rather than modeling geometry, materials, or lighting."], "52": ["Furthermore, to support interactive semantic manipulation, we extend our method in two directions.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "Furthermore, to support interactive semantic manipula- tion, we extend our method in two directions."], "53": ["First, we use instance level object segmentation information, which can separate different object instances within the same category.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "First, we use instance-level object segmentation information, which can separate different object instances within the same cat- egory."], "54": ["This enables flexible object manipulations, such as adding/removing objects and changing object types.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "This enables \ufb02exible object manipulations, such as adding/removing objects and changing object types."], "55": ["Second, we propose a method to generate diverse results given the same input label map, allowing the user to edit the appearance of the same object interactively.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "Second, we propose a method to generate di- verse results given the same input, allowing users to edit the object appearance interactively."], "56": ["We compare against state-of-the-art visual synthesis systems and show that our method outperforms these approaches regarding both quantitative evaluations and hu- man perception studies.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "We compare against state-of-the-art visual synthesis sys- tems [5, 21], and show that our method outperforms these approaches regarding both quantitative evaluations and hu- man perception studies."], "57": ["We also perform an ablation study regarding the training objectives and the importance of instance-level segmentation information.", "plag", "https://arxiv.org/pdf/1711.11585v2.pdf", "We also perform an ablation study regarding the training objectives and the importance of instance-level segmentation information."], "58": ["In addition to se- mantic manipulation, we test our method on edge2photo ap- plications, which shows the generalizability of our approach.", "notplag", "none", "none"], "59": ["What is our Pitch?", "notplag", "none", "none"], "60": ["For Businesses:", "notplag", "none", "none"], "61": [" Save money through digitization", "notplag", "none", "none"], "62": [" Connect businesses with their customers directly, every time a document is uploaded by a business for a customers transaction", "notplag", "none", "none"], "63": [" Collect and share Word-of-mouth recommendations about their businesses / services to their connections connections", "notplag", "none", "none"], "64": [" Build Brand and online presence", "notplag", "none", "none"], "65": [" Retain and Enhance customer loyalty and customer base", "notplag", "none", "none"], "66": [" Cross-sell allied products / services (warranty, AMC, warranty / AMC renewals, DVD players for TV, )", "notplag", "none", "none"], "67": [" Reminders for timely services  Automobiles, Insurance, ", "notplag", "none", "none"], "68": [" Emotional value  Save environment", "notplag", "none", "none"], "69": ["For Consumers:", "notplag", "none", "none"], "70": [" Digitize documents, reduce clutter, avoid printing and Save environment", "notplag", "none", "none"], "71": [" Invite friends & family, build your own community of trust, share digital", "notplag", "none", "none"], "72": [" Only one copy of the digital document to avoid", "notplag", "none", "none"], "73": ["", "notplag", "none", "none"], "74": ["Manage documents centrally  one stop storage of all documents (invoices, warranty, user manual, insurance, )", "notplag", "none", "none"], "75": [" Access from anywhere anytime using a device of choice  Cloud enabled; web and mobile apps", "notplag", "none", "none"], "76": [" Never miss any critical actions  warrant renewals, timely service of the devices / automobiles, insurance payments, ", "notplag", "none", "none"], "77": [" Connect directly with businesses ", "notplag", "none", "none"], "78": [" Build your own community of trust, leverage the recommendations from trusted connections while making important decisions (buy / sell )", "notplag", "none", "none"]}}
  return jsonify(posts)


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER']), exist_ok=True)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

    sse.ConvertUserDoc(app.config['UPLOAD_FOLDER']+'/'+f.filename)

    os.remove(app.config['UPLOAD_FOLDER']+'/'+f.filename)

    return jsonify({'status':'file uploaded successfully'})
  return jsonify({'status':'file uploaded FAILED'})


if __name__ == "__main__":
    app.run(debug="True")



