---
title: Conference Program
layout: schedule
excerpt: "ACL 2017 conference program."
permalink: /confprogramtest2
sidebar: false
script: |
    <script type="text/javascript">
        $(document).ready(function() {

            $('[class$="-details"]').hide();

            $('body').on('click', 'div.session-expandable', function(event) {
                event.preventDefault();
                $(this).children('[class$="-details"]').slideToggle();
                $(this).children('#expander').toggleClass('expanded');
            });


            $('body').on('click', 'div.session-title', function(event) {
                event.preventDefault();
                $(this).children('[class$="-details"]').slideToggle();
                $(this).children('#expander').toggleClass('expanded');
            });

            $('body').on('click', 'a.inline-location', function(event) {
                return false;
            });

            $('body').on('click', 'a.session-location', function(event) {
                return false;
            });

            $('body').on('click', 'a.info-button', function(event) {
                return false;
            });

            $('body').on('click', 'a.info-link', function(event) {
                event.stopPropagation();
            });

        });
    </script>
---
{% include base_path %}

<div class="schedule">
    <div class="day" id="first-day">Sunday, June 12</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time">9:30 AM &ndash; 12:30 PM</span><br/>
        <div class="tutorial-session-details">
            <ul>
                <li>
                    <span class="tutorial-title">[T1] English Resource Semantics</span><br/>
                    <a href="#" class="btn btn--location inline-location">Executive 3AB</a>
                </li>
                <li>
                 <span class="tutorial-title">[T2] Multilingual Multimodal Language Processing Using Neural Networks</span><br/>
                 <a href="#" class="btn btn--location inline-location">Spinnaker</a>
             </li>
             <li>
                <span class="tutorial-title">[T3] Question Answering with Knowledge Base, Web and Beyond</span><br/>
                <a href="#" class="btn btn--location inline-location">Marina 3</a></li>
            </ul>      
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 2:00 PM</span>
    </div>
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>        
        <span class="session-time">2:00 PM &ndash; 5:00 PM</span>
        <div class="tutorial-session-details">
            <ul>
                <li>
                    <span class="tutorial-title">[T4] Recent Progress in Deep Learning for NLP</span><br/>
                    <a href="#" class="btn btn--location inline-location">Spinnaker</a>
                </li>
                <li>
                 <span class="tutorial-title">[T5] Scalable Statistical Relational Learning for NLP</span><br/>
                 <a href="#" class="btn btn--location inline-location">Marina 3</a>
             </li>
             <li>
                <span class="tutorial-title">[T6] Statistical Machine Translation between Related Languages</span><br/>
                <a href="#" class="btn btn--location inline-location">Executive 3AB</a></li>
            </ul>      
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Welcome Reception</span><br/>        
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span>
        <span class="session-location btn btn--location">Grande Foyer &amp; Terrace</span>
    </div>
    <div class="day" id="first-day">Monday, June 13</div>
    <div class="session session-plenary">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Welcome</span><br/>        
        <span class="session-people">Kevin Knight, Ani Nenkova, Owen Rambow</span><br/>
        <span class="session-time">9:00 AM &ndash; 9:15 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: "How can NLP help cure cancer?"</a><br/>        
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <div class="session-abstract">

                <p>Cancer inflicts a heavy toll on our society. One out of seven women will be diagnosed with breast cancer during their lifetime, a fraction of them contributing to about 450,000 deaths annually worldwide. Despite billions of dollars invested in cancer research, our understanding of the disease, treatment, and prevention is still limited.</p>

                <p>Majority of cancer research today takes place in biology and medicine. Computer science plays a minor supporting role in this process if at all. In this talk, I hope to convince you that NLP as a field has a chance to play a significant role in this battle. Indeed, free-form text remains the primary means by which physicians record their observations and clinical findings. Unfortunately, this rich source of textual information is severely underutilized by predictive models in oncology. Current models rely primarily only on structured data.</p>

                <p>In the first part of my talk, I will describe a number of tasks where NLP-based models can make a difference in clinical practice. For example, these include improving models of disease progression, preventing over-treatment, and narrowing down to the cure. This part of the talk draws on active collaborations with oncologists from Massachusetts General Hospital (MGH).</p>

                <p>In the second part of the talk, I will push beyond standard tools, introducing new functionalities and avoiding annotation-hungry training paradigms ill-suited for clinical practice. In particular, I will focus on interpretable neural models that provide rationales underlying their predictions, and semi-supervised methods for information extraction.</p>
            </div>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:30 AM &ndash; 11:00 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-1a">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation I</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: David Chiang</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">Achieving Accurate Conclusions in Evaluation of Automatic Machine Translation Metrics. </span><em>Yvette Graham and Qun Liu</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td><span class="paper-title">Flexible Non-Terminals for Dependency Tree-to-Tree Reordering. </span> <em>John Richardson, Fabien Cromieres, Toshiaki Nakazawa and Sadao Kurohashi</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td><span class="paper-title">Selecting Syntactic, Non-redundant Segments in Active Learning for Machine Translation. </span><em>Akiva Miura, Graham Neubig, Michael Paul and Satoshi Nakamura</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:10</td>
                    <td><span class="paper-title">Multi-Source Neural Translation. </span><em>Barret Zoph and Kevin Knight</em></td>
                </tr>
                <tr>
                    <td>12:10–12:20</td>
                    <td><span class="paper-title">Controlling Politeness in Neural Machine Translation via Side Constraints. </span><em>Rico Sennrich, Barry Haddow and Alexandra Birch</em></td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td><span class="paper-title">An Empirical Evaluation of Noise Contrastive Estimation for the Neural Network Joint Model of Translation. </span><em>Colin Cherry</em></td>
                </tr>                
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-1b">
        <div id="expander"></div><a href="#" class="session-title">Summarization</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Fei Liu</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">Neural Network-Based Abstract Generation for Opinions and Arguments. </span><em>Lu Wang and Wang Ling</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td>
                        <span class="paper-title">A Low-Rank Approximation Approach to Learning Joint Embeddings of News Stories and Images for Timeline Summarization. </span><em>William Yang Wang, Yashar Mehdad, Dragomir Radev and Amanda Stent</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td>
                        <span class="paper-title">Entity-balanced Gaussian pLSA for Automated Comparison. </span><em>Danish Contractor, Parag Singla and Mausam</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:10</td>
                    <td>
                        <span class="paper-title">Automatic Summarization of Student Course Feedback. </span><em>Wencan Luo, Fei Liu, Zitao Liu and Diane Litman</em>
                    </td>
                </tr>
                <tr>
                    <td>12:10–12:20</td>
                    <td>
                        <span class="paper-title">Abstractive Sentence Summarization with Attentive Recurrent Neural Networks. </span><em>Sumit Chopra, Michael Auli and Alexander M. Rush</em>
                    </td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td>
                        <span class="paper-title">Knowledge-Guided Linguistic Rewrites for Inference Rule Verification. </span><em>Prachi Jain and Mausam</em>
                    </td>
                </tr>
            </table>
        </div> 
    </div>
    <div class="session session-expandable session-papers3" id="session-1c">
        <div id="expander"></div><a href="#" class="session-title">Dialog</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mari Ostendorf</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">Integer Linear Programming for Discourse Parsing. </span><em>Jérémy Perret, Stergos Afantenos, Nicholas Asher and Mathieu Morey</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td>
                        <span class="paper-title">A Diversity-Promoting Objective Function for Neural Conversation Models. </span><em>Jiwei Li, Michel Galley, Chris Brockett, Jianfeng Gao and Bill Dolan</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td>
                        <span class="paper-title">Multi-domain Neural Network Language Generation for Spoken Dialogue Systems. </span><em>Tsung-Hsien Wen, Milica Gasic, Nikola Mrkšić, Lina M. Rojas Barahona, Pei-Hao Su, David Vandyke and Steve Young</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:10</td>
                    <td>
                        <span class="paper-title">A Long Short-Term Memory Framework for Predicting Humor in Dialogues. </span><em>Dario Bertero and Pascale Fung</em>
                    </td>
                </tr>
                <tr>
                    <td>12:10–12:20</td>
                    <td>
                        <span class="paper-title">Conversational Flow in Oxford-style Debates. </span><em>Justine Zhang, Ravi Kumar, Sujith Ravi and Cristian Danescu-Niculescu-Mizil</em>
                    </td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td>
                        <span class="paper-title">Counter-fitting Word Vectors to Linguistic Constraints. </span><em>Nikola Mrkšić, Diarmuid Ó Séaghdha, Blaise Thomson, Milica Gasic, Lina M. Rojas Barahona, Pei-Hao Su, David Vandyke, Tsung-Hsien Wen and Steve Young</em>
                    </td>
                </tr>
            </table>
        </div> 
    </div>
    <div class="session session-plenary">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 2:00 PM</span>
    </div>    
    <div class="session session-expandable session-papers1" id="session-2a">
        <div id="expander"></div><a href="#" class="session-title">Language and Vision</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Meg Mitchell</td>
                </tr>
                <tr>
                    <td>2:00–2:20</td>
                    <td>
                        <span class="paper-title">Grounded Semantic Role Labeling. </span><em>Shaohua Yang, Qiaozi Gao, Changsong Liu, Caiming Xiong, Song-Chun Zhu and Joyce Chai</em>
                    </td>
                </tr>
                <tr>
                    <td>2:20–2:40</td>
                    <td>
                        <span class="paper-title">Black Holes and White Rabbits: Metaphor Identification with Visual Features. </span><em>Ekaterina Shutova, Douwe Kiela and Jean Maillard</em>
                    </td>
                </tr>
                <tr>
                    <td>2:40–3:00</td>
                    <td>
                        <span class="paper-title">Bridge Correlational Neural Networks for Multilingual Multimodal Representation Learning. </span><em>Janarthanan Rajendran, Mitesh M Khapra, Sarath Chandar and Balaraman Ravindran</em>
                    </td>
                </tr>
                <tr>
                    <td>3:00–3:20</td>
                    <td>
                        <span class="paper-title">Unsupervised Visual Sense Disambiguation for Verbs using Multimodal Embeddings. </span><em>Spandana Gella, Mirella Lapata and Frank Keller</em>
                    </td>
                </tr>
                <tr>
                    <td>3:20–3:30</td>
                    <td>
                        <span class="paper-title">Stating the Obvious: Extracting Visual Common Sense Knowledge. </span><em>Mark Yatskar, Vicente Ordonez and Ali Farhadi</em>
                    </td>
                </tr>
            </table>                
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-2b">
        <div id="expander"></div><a href="#" class="session-title">Parsing</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Alexander Rush</td>
                </tr>
                <tr>
                    <td>2:00–2:20</td>
                    <td>
                        <span class="paper-title">Efficient Structured Inference for Transition-Based Parsing with Neural Networks and Error States. </span><em>Ashish Vaswani and Kenji Sagae</em>
                    </td>
                </tr>
                <tr>
                    <td>2:20–2:40</td>
                    <td>
                        <span class="paper-title">Recurrent Neural Network Grammars. </span><em>Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros and Noah A. Smith</em>
                    </td>
                </tr>
                <tr>
                    <td>2:40–3:00</td>
                    <td>
                        <span class="paper-title">Expected F-Measure Training for Shift-Reduce Parsing with Recurrent Neural Networks. </span><em>Wenduan Xu, Michael Auli and Stephen Clark</em>
                    </td>
                </tr>
                <tr>
                    <td>3:00–3:20</td>
                    <td>
                        <span class="paper-title">LSTM CCG Parsing. </span><em>Mike Lewis, Kenton Lee and Luke Zettlemoyer</em>
                    </td>
                </tr>
                <tr>
                    <td>3:20–3:30</td>
                    <td>
                        <span class="paper-title">Supertagging With LSTMs. </span><em>Ashish Vaswani, Yonatan Bisk, Kenji Sagae and Ryan Musa</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-2c">
        <div id="expander"></div><a href="#" class="session-title">Named Entity Recognition</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Alessandro Moschitti</td>
                </tr>
                <tr>
                    <td>2:00–2:20</td>
                    <td>
                        <span class="paper-title">An Empirical Study of Automatic Chinese Word Segmentation for Spoken Language Understanding and Named Entity Recognition. </span><em>Wencan Luo and Fan Yang</em>
                    </td>
                </tr>
                <tr>
                    <td>2:20–2:40</td>
                    <td>
                        <span class="paper-title">Name Tagging for Low-resource Incident Languages based on Expectation-driven Learning. </span><em>Boliang Zhang, Xiaoman Pan, Tianlu Wang, Ashish Vaswani, Heng Ji, Kevin Knight and Daniel Marcu</em>
                    </td>
                </tr>
                <tr>
                    <td>2:40–3:00</td>
                    <td>
                        <span class="paper-title">Neural Architectures for Named Entity Recognition. </span><em>Guillaume Lample, Miguel Ballesteros, Kazuya Kawakami, Sandeep Subramanian and Chris Dyer</em>
                    </td>
                </tr>
                <tr>
                    <td>3:00–3:20</td>
                    <td>
                        <span class="paper-title">Dynamic Feature Induction: The Last Gist to the State-of-the-Art. </span><em>Jinho D. Choi</em>
                    </td>
                </tr>
                <tr>
                    <td>3:20–3:30</td>
                    <td>
                        <span class="paper-title">Drop-out Conditional Random Fields for Twitter with Huge Mined Gazetteer. </span><em>Eun-Suk Yang, Young-Bum Kim, Ruhi Sarikaya and Yu-Seop Kim</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:30 PM &ndash; 4:00 PM</span>
    </div>   
    <div class="session session-expandable session-papers1" id="session-3a">
        <div id="expander"></div><a href="#" class="session-title">Event Detection</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Heng Ji</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">Joint Extraction of Events and Entities within a Document Context. </span><em>Bishan Yang and Tom Mitchell</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">A Hierarchical Distance-dependent Bayesian Model for Event Coreference Resolution. </span><em>Bishan Yang, Claire Cardie and Peter Frazier</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–5:00</td>
                    <td>
                        <span class="paper-title">Joint Event Extraction via Recurrent Neural Networks. </span><em>Thien Huu Nguyen, Kyunghyun Cho and Ralph Grishman</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-3b">
        <div id="expander"></div><a href="#" class="session-title">Language Models</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Chris Dyer</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">Top-down Tree Long Short-Term Memory Networks. </span><em>Xingxing Zhang, Liang Lu, Mirella Lapata</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">Recurrent Memory Networks for Language Modeling. </span><em>Ke Tran, Arianna Bisazza, Christof Monz</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–5:00</td>
                    <td>
                        <span class="paper-title">A Latent Variable Recurrent Neural Network for Discourse-Driven Language Models. </span><em>Yangfeng Ji, Gholamreza Haffari, Jacob Eisenstein</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-3c">
        <div id="expander"></div><a href="#" class="session-title">Non-literal Language</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Marie-Catherine de Marneffe</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">Questioning Arbitrariness in Language: a Data-Driven Study of Conventional Iconicity. </span><em>Ekaterina Abramova and Raquel Fernandez</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">Distinguishing Literal and Non-Literal Usage of German Particle Verbs. </span><em>Maximilian Köper and Sabine Schulte im Walde</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–5:00</td>
                    <td>
                        <span class="paper-title">Phrasal Substitution of Idiomatic Expressions. </span><em>Changsheng Liu and Rebecca Hwa</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">5:00 PM &ndash; 5:15 PM</span>
    </div>  
    <div class="session session-expandable session-plenary">
        <div id="expander"></div><a href="#" class="session-title">One-Minute Madness</a><br/>        
        <span class="session-time">5:15 PM &ndash; 6:00 PM</span><br/>
        <div class="paper-session-details">
            <div class="session-abstract">
                <p>Chair: Joel Tetreault</p>

                <p>Prior to the poster session, TACL and long-paper poster presenters will be given one minute each to pitch their paper. The poster session will immediately follow these presentations along with a buffet dinner.</p>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-plenary">
    <div id="expander"></div><a href="#" class="session-title">Posters, Demos & Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
        <div class="paper-session-details">
            <span class="info-button btn btn--small">Main Conference</span>
            <table class="paper-table">
                <tr>
                    <td>
                        <span class="paper-title">A Recurrent Neural Networks Approach for Estimating the Quality of Machine Translation Output. </span><em>Hyun Kim and Jong-Hyeok Lee</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Agreement on Target-bidirectional Neural Machine Translation. </span><em>Lemao Liu, Masao Utiyama, Andrew Finch and Eiichiro Sumita</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">An Unsupervised Model of Orthographic Variation for Historical Document Transcription. </span><em>Dan Garrette and Hannah Alpert-Abrams</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Bidirectional RNN for Medical Event Detection in Electronic Health Records. </span><em>Abhyuday Jagannatha and Hong Yu</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Breaking the Closed World Assumption in Text Classification. </span><em>Geli Fei and Bing Liu</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Building Chinese Affective Resources in Valence-Arousal Dimensions. </span><em>Liang-Chih Yu, Lung-Hao Lee, Shuai Hao, Jin Wang, Yunchao He, Jun Hu, K. Robert Lai and Xuejie Zhang</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Combining Recurrent and Convolutional Neural Networks for Relation Classification. </span><em>Ngoc Thang Vu, Heike Adel, Pankaj Gupta and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Conversational Markers of Constructive Discussions. </span><em>Vlad Niculae and Cristian Danescu-Niculescu-Mizil</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Cross-lingual Wikification Using Multilingual Embeddings. </span><em>Chen-Tse Tsai and Dan Roth</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Deconstructing Complex Search Tasks: a Bayesian Nonparametric Approach for Extracting Sub-tasks. </span><em>Rishabh Mehrotra, Prasanta Bhattacharya and Emine Yilmaz</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Expectation-Regulated Neural Model for Event Mention Extraction. </span><em>Ching-Yun Chang, Zhiyang Teng and Yue Zhang</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Grammatical error correction using neural machine translation. </span><em>Zheng Yuan and Ted Briscoe</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Improved Neural Network-based Multi-label Classification with Better Initialization Leveraging Label Co-occurrence. </span><em>Gakuto Kurata, Bing Xiang and Bowen Zhou</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Improving event prediction by representing script participants. </span><em>Simon Ahrendt and Vera Demberg</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Individual Variation in the Choice of Referential Form. </span><em>Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Inferring Psycholinguistic Properties of Words. </span><em>Gustavo Paetzold and Lucia Specia</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Intra-Topic Variability Normalization based on Linear Projection for Topic Classification. </span><em>Quan Liu, Wu Guo, Zhen-Hua Ling, Hui Jiang and Yu Hu</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Joint Learning Templates and Slots for Event Schema Induction. </span><em>Lei Sha, Sujian Li, Baobao Chang, Zhifang Sui and Zhifang Sui</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Large-scale Multitask Learning for Machine Translation Quality Estimation. </span><em>Kashif Shah and Lucia Specia</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Learning Distributed Word Representations For Bidirectional LSTM Recurrent Neural Network. </span><em>Peilu Wang, Yao Qian, Frank Soong, Lei He and Hai Zhao</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Leverage Financial News to Predict Stock Price Movements Using Word Embeddings and Deep Neural Networks. </span><em>Yangtuo Peng and Hui Jiang</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Multimodal Semantic Learning from Child-Directed Input. </span><em>Angeliki Lazaridou, Grzegorz Chrupała, Raquel Fernandez and Marco Baroni</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Online Multilingual Topic Models with Multi-Level Hyperpriors. </span><em>Kriste Krstovski, David Smith and Michael J. Kurtz</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Psycholinguistic Features for Deceptive Role Detection in Werewolf. </span><em>Codruta Girlea, Roxana Girju and Eyal Amir</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Recurrent Support Vector Machines For Slot Tagging In Spoken Language Understanding. </span><em>Yangyang Shi, Kaisheng Yao, Hu Chen, Dong Yu, Yi-Cheng Pan and Mei-Yuh Hwang</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">STransE: a novel embedding model of entities and relationships in knowledge bases. </span><em>Dat Quoc Nguyen, Kairit Sirts, Lizhen Qu and Mark Johnson</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Sequential Short-Text Classification with Recurrent and Convolutional Neural Networks. </span><em>Ji Young Lee and Franck Dernoncourt</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Shift-Reduce CCG Parsing using Neural Network Models. </span><em>Bharat Ram Ambati, Tejaswini Deoskar and Mark Steedman</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Structured Prediction with Output Embeddings for Semantic Image Annotation. </span><em>Ariadna Quattoni, Arnau Ramisa, Pranava Swaroop Madhyastha, Edgar Simo-Serra and Francesc Moreno-Noguer</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Symmetric Patterns and Coordinations: Fast and Enhanced Representations of Verbs and Adjectives. </span><em>Roy Schwartz, Roi Reichart and Ari Rappoport</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">The Sensitivity of Topic Coherence Evaluation to Topic Cardinality. </span><em>Jey Han Lau and Timothy Baldwin</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Transition-Based Syntactic Linearization with Lookahead Features. </span><em>Ratish Puduppully, Yue Zhang and Manish Shrivastava</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Vision and Feature Norms: Improving automatic feature norm learning through cross-modal maps. </span><em>Luana Bulat, Douwe Kiela and Stephen Clark</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small">Student Research Workshop</span>
            <table class="paper-table">
                <tr>
                    <td>
                        <span class="paper-title">An End-to-end Approach to Learning Semantic Frames with Feedforward Neural Network. </span><em>Yukun Feng, Yipei Xu and Dong Yu</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Analogy-based detection of morphological and semantic relations with word embeddings: what works and what doesn't. </span><em>Anna Gladkova, Aleksandr Drozd and Satoshi Matsuoka</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Argument Identification in Chinese Editorials. </span><em>Marisa Chow</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Automatic tagging and retrieval of E-Commerce products based on visual features. </span><em>Vasu Sharma and Harish Karnick</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Combining syntactic patterns and Wikipedia's hierarchy of hyperlinks to extract relations: The case of meronymy extraction. </span><em>Debela Tesfaye Gemechu, Michael Zock and Solomon Teferra</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Data-driven Paraphrasing and Stylistic Harmonization. </span><em>Gerold Hintz</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Detecting 'Smart' Spammers on Social Network: A Topic Model Approach. </span><em>Linqing Liu, Yao Lu, Ye Luo, Renxian Zhang, Laurent Itti and Jianwei Lu</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Developing language technology tools and resources for a resource-poor language: Sindhi. </span><em>Raveesh Motlani</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small">System Demonstrations</span>
            <table class="paper-table">
                <tr>
                    <td>
                        <span class="paper-title">Illinois Math Solver: Math Reasoning on the Web. </span><em>Subhro Roy and Dan Roth</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">LingoTurk: managing crowdsourced tasks for psycholinguistics. </span><em>Florian Pusse, Asad Sayeed and Vera Demberg</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Sentential Paraphrasing as Black-Box Machine Translation. </span><em>Courtney Napoles, Chris Callison-Burch and Matt Post</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">A Tag-based English Math Word Problem Solver with Understanding, Reasoning and Explanation. </span><em>Chao-Chun Liang, Kuang-Yi Hsu, Chien-Tsung Huang, Chung-Min Li, Shen-Yu Miao and Keh-Yih Su</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Cross-media Event Extraction and Recommendation. </span><em>Di Lu, Clare Voss, Fangbo Tao, Xiang Ren, Rachel Guan, Rostyslav Korolov, Tongtao Zhang, Dongang Wang, Hongzhi Li, Taylor Cassidy, Heng Ji, Shih-fu Chang, Jiawei Han, William Wallace, James Hendler, Mei Si and Lance Kaplan</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">SODA: Service Oriented Domain Adaptation Architecture for Microblog Categorization. </span><em>Himanshu Sharad Bhatt, Sandipan Dandapat, Peddamuthu Balaji, Shourya Roy, Sharmistha Jat and Deepali Semwal</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Lecture Translator - Speech translation framework for simultaneous lecture translation. </span><em>Markus Müller, Thai Son Nguyen, Jan Niehues, Eunah Cho, Bastian Krüger, Thanh-Le Ha, Kevin Kilgour, Matthias Sperber, Mohammed Mediani, Sebastian Stüker and Alex Waibel</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Zara The Supergirl: An Empathetic Personality Recognition System. </span><em>Pascale Fung, Anik Dey, Farhad Bin Siddique, Ruixi Lin, Yang Yang, Yan Wan and Ho Yin Ricky Chan</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Kathaa: A Visual Programming Framework for NLP Applications. </span><em>Sharada Prasanna Mohanty, Nehal J Wani, Manish Srivastava and Dipti Misra Sharma</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">"Why Should I Trust You?": Explaining the Predictions of Any Classifier. </span><em>Marco Ribeiro, Sameer Singh and Carlos Guestrin</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-plenary">
        <div id="expander"></div><a href="#" class="session-title">Social Event</a><br/>        
        <span class="session-time">8:00 PM &ndash; 10:00 PM</span>
        <div class="paper-session-details">
            <div class="session-abstract">
                
                <span class="info-button btn btn--small">Included in registration</span>

                <p>Enjoy a fun evening under the stars!</p>

                <p>Bring your Flower Power to our SoCal Beach Party! After the main dinner and Poster Session, join us on the Bayview Lawn adjacent to the Pavilion for desserts, coffee, tea, and drinks (cash bar). A Beach Boys style band will entertain you when you are not busy in the VW Bus Photo Booth, talking amongst your friends and colleagues, or playing with the beach balls.</p>

                <p>Learn more about the social event <a class="info-link" target="_blank" href="http://naacl.org/naacl-hlt-2016/social_event.html">here</a>.</p>
            </div>
        </div>
    </div>
</div>
