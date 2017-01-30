---
title: Conference Program
layout: schedule
excerpt: "ACL 2017 conference program."
permalink: /confprogramtest2
sidebar: false
script: |
    <script type="text/javascript">
        $(document).ready(function() {

            $(".session-details").hide();

            $('body').on('click', 'div.session-expandable', function(event) {
                event.preventDefault();
                $(this).children('.session-details').slideToggle();
                $(this).children('.session-title').toggleClass('expanded');
            });

            $('body').on('click', 'div.session-title', function(event) {
                event.preventDefault();
                $(this).children('.session-details').slideToggle();
                $(this).children('.session-title').toggleClass('expanded');
            });

            $('body').on('click', 'a.inline-location', function(event) {
                return false;
            });

            $('body').on('click', 'a.session-location', function(event) {
                return false;
            });
        });
    </script>
---
{% include base_path %}

<div class="schedule">
    <div class="day" id="first-day">Sunday, June 12</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials">
        <a href="#" class="session-title">Morning Tutorials</a><br/>        
        <span class="session-time">9:30 AM &ndash; 12:30 PM</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Afternoon Tutorials</a><br/>        
        <span class="session-time">2:00 PM &ndash; 5:00 PM</span>
        <div class="session-details">
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
    <div class="session session-tutorials">
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
        <a href="#" class="session-title">Invited Talk: "How can NLP help cure cancer?"</a><br/>        
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Machine Translation I</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Summarization</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Dialog</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Language and Vision</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Parsing</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Named Entity Recognition</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Event Detection</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Language Models</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="session-details">
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
        <a href="#" class="session-title">Non-literal Language</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="session-details">
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
        <a href="#" class="session-title">One-Minute Madness</a><br/>        
        <span class="session-time">5:15 PM &ndash; 6:00 PM</span>
        <div class="session-details">
            <div class="session-abstract">
                
                <p>Chair: Joel Tetreault</p>

                <p>Prior to the poster session, TACL and long-paper poster presenters will be given one minute each to pitch their paper. The poster session will immediately follow these presentations along with a buffet dinner.</p>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-plenary">
    <a href="#" class="session-title">Posters, Demos & Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
        <div class="session-details">
        </div>
    </div>
</div>
