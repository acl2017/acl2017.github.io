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

            $('body').on('click', 'div.session-abstract', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.paper-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', '.tutorial-session-details ul', function(event) {
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
    <div class="day" id="second-day">Monday, June 13</div>
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
    <div class="session session-expandable session-plenary" id="session-invited-regina">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: "How can NLP help cure cancer?"</a><br/>        
        <span class="session-people">Regina Barzilay</span><br/>
        <span class="session-time">9:15 AM &ndash; 10:30 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
            <hr class="detail-separator"/>
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
        <span class="session-time">5:15 PM &ndash; 6:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Chair: Joel Tetreault</p>

                <p>Prior to the poster session, TACL and long-paper poster presenters will be given one minute each to pitch their paper. The poster session will immediately follow these presentations along with a buffet dinner.</p>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-first-poster">
        <div id="expander"></div><a href="#" class="session-title">Posters, Demos &amp; Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
        <span class="session-location btn btn--location">Pavilion</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
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
                        <span class="paper-title">rstWeb - A Browser-based Annotation Interface for Rhetorical Structure Theory and Discourse Relations. </span><em>Amir Zeldes</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Instant Feedback for Increasing the Presence of Solutions in Peer Reviews. </span><em>Huy Nguyen, Wenting Xiong and Diane Litman</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Farasa: A Fast and Furious Segmenter for Arabic. </span><em>Ahmed Abdelali, Kareem Darwish, Nadir Durrani and Hamdy Mubarak</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">iAppraise: A Manual Machine Translation Evaluation Environment Supporting Eye-tracking. </span><em>Ahmed Abdelali, Nadir Durrani and Francisco Guzmán</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Linguistica 5: Unsupervised Learning of Linguistic Structure. </span><em>Jackson Lee and John Goldsmith</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">TransRead: Designing a Bilingual Reading Experience with Machine Translation Technologies. </span><em>François Yvon, Yong Xu, Marianna Apidianaki, Clément Pillias and Pierre Cubaud</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">New Dimensions in Testimony Demonstration. </span><em>Ron Artstein, Alesia Gainer, Kallirroi Georgila, Anton Leuski, Ari Shapiro and David Traum</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">ArgRewrite: A Web-based Revision Assistant for Argumentative Writings. </span><em>Fan Zhang, Rebecca Hwa, Diane Litman and Homa B. Hashemi</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Scaling Up Word Clustering. </span><em>Jon Dehdari, Liling Tan and Josef van Genabith</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Task Completion Platform: A self-serve multi-domain goal oriented dialogue platform. </span><em>Paul Crook, Alex Marin, Vipul Agarwal, Khushboo Aggarwal, Tasos Anastasakos, Ravi Bikkula, Daniel Boies, Asli Celikyilmaz, Senthilkumar Chandramohan, Zhaleh Feizollahi, Roman Holenstein, Minwoo Jeong, Omar Khan, Young-Bum Kim, Elizabeth Krawczyk, Xiaohu Liu, Danko Panic, Vasiliy Radostev, Nikhil Ramesh, Jean-Phillipe Robichaud, Alexandre Rochette, Logan Stromberg and Ruhi Sarikaya</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="day" id="third-day">Tuesday, June 14</div>
    <div class="session session-plenary">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-4a">
        <div id="expander"></div><a href="#" class="session-title">Semantic Parsing</a><br/>
        <span class="session-time">9:00 AM &ndash; 10:30 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mike Lewis</td>
                </tr>
                <tr>
                    <td>9:00–9:20</td>
                    <td>
                        <span class="paper-title">Transforming Dependency Structures to Logical Forms for Semantic Parsing. </span><em>Siva Reddy, Oscar Täckström, Michael Collins, Tom Kwiatkowski, Dipanjan Das, Mark Steedman and Mirella Lapata</em>
                    </td>
                </tr>
                <tr>
                    <td>9:20–9:40</td>
                    <td>
                        <span class="paper-title">Imitation Learning of Agenda-based Semantic Parsers. </span><em>Jonathan Berant and Percy Liang</em>
                    </td>
                </tr>
                <tr>
                    <td>9:40–10:00</td>
                    <td>
                        <span class="paper-title">Probabilistic Models for Learning a Semantic Parser Lexicon. </span><em>Jayant Krishnamurthy</em>
                    </td>
                </tr>
                <tr>
                    <td>10:00–10:20</td>
                    <td>
                        <span class="paper-title">Semantic Parsing of Ambiguous Input through Paraphrasing and Verification. </span><em>Philip Arthur, Graham Neubig, Sakriani Sakti, Tomoki Toda and Satoshi Nakamura</em>
                    </td>
                </tr>
                <tr>
                    <td>10:20–10:30</td>
                    <td>
                        <span class="paper-title">Unsupervised Compound Splitting With Distributional Semantics Rivals Supervised Methods. </span><em>Martin Riedl and Chris Biemann</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-4b">
        <div id="expander"></div><a href="#" class="session-title">Morphology & Phonology</a><br/>
        <span class="session-time">9:00 AM &ndash; 10:30 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Dilek Hakkani-Tur</td>
                </tr>
                <tr>
                    <td>9:00–9:20</td>
                    <td>
                        <span class="paper-title">Weighting Finite-State Transductions With Neural Context. </span><em>Pushpendre Rastogi, Ryan Cotterell and Jason Eisner</em>
                    </td>
                </tr>
                <tr>
                    <td>9:20–9:40</td>
                    <td>
                        <span class="paper-title">Morphological Inflection Generation Using Character Sequence to Sequence Learning. </span><em>Manaal Faruqui, Yulia Tsvetkov, Graham Neubig and Chris Dyer</em>
                    </td>
                </tr>
                <tr>
                    <td>9:40–10:00</td>
                    <td>
                        <span class="paper-title">Towards Unsupervised and Language-independent Compound Splitting using Inflectional Morphological Transformations. </span><em>Patrick Ziering and Lonneke van der Plas</em>
                    </td>
                </tr>
                <tr>
                    <td>10:00–10:20</td>
                    <td>
                        <span class="paper-title">Phonological Pun-derstanding. </span><em>Aaron Jaech, Rik Koncel-Kedziorski and Mari Ostendorf</em>
                    </td>
                </tr>
                <tr>
                    <td>10:20–10:30</td>
                    <td>
                        <span class="paper-title">A Joint Model of Orthography and Morphological Segmentation. </span><em>Ryan Cotterell, Tim Vieira and Hinrich Schütze</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-4c">
        <div id="expander"></div><a href="#" class="session-title">Various</a><br/>
        <span class="session-time">9:00 AM &ndash; 10:30 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Jinho Choi</td>
                </tr>
                <tr>
                    <td>9:00–9:20</td>
                    <td>
                        <span class="paper-title">Syntactic Parsing of Web Queries with Question Intent. </span><em>Yuval Pinter, Roi Reichart and Idan Szpektor</em>
                    </td>
                </tr>
                <tr>
                    <td>9:20–9:40</td>
                    <td>
                        <span class="paper-title">Visualizing and Understanding Neural Models in NLP. </span><em>Jiwei Li, Xinlei Chen, Eduard Hovy and Dan Jurafsky</em>
                    </td>
                </tr>
                <tr>
                    <td>9:40–10:00</td>
                    <td>
                        <span class="paper-title">Bilingual Word Embeddings from Parallel and Non-parallel Corpora for Cross-Language Text Classification. </span><em>Aditya Mogadala and Achim Rettinger</em>
                    </td>
                </tr>
                <tr>
                    <td>10:00–10:20</td>
                    <td>
                        <span class="paper-title">Joint Learning with Global Inference for Comment Classification in Community Question Answering. </span><em>Shafiq Joty, Lluís Màrquez and Preslav Nakov</em>
                    </td>
                </tr>
                <tr>
                    <td>10:20–10:30</td>
                    <td>
                        <span class="paper-title">Weak Semi-Markov CRFs for Noun Phrase Chunking in Informal Text Aldrian. </span><em>Obaja Muis and Wei Lu</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:30 AM &ndash; 11:00 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-5a">
        <div id="expander"></div><a href="#" class="session-title">Generation</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Lu Wang</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">What to talk about and how? Selective Generation using LSTMs with Coarse-to-Fine Alignment. </span><em>Hongyuan Mei, Mohit Bansal and Matthew Walter</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td>
                        <span class="paper-title">Generation from Abstract Meaning Representation using Tree Transducers. </span><em>Jeffrey Flanigan, Chris Dyer, Noah A. Smith and Jaime Carbonell</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td>
                        <span class="paper-title">A Corpus and Semantic Parser for Multilingual Natural Language Querying of OpenStreetMap. </span><em>Carolin Haas and Stefan Riezler</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:20</td>
                    <td>
                        <span class="paper-title">Natural Language Communication with Robots. </span><em>Yonatan Bisk, Daniel Marcu and Deniz Yuret</em>
                    </td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td>
                        <span class="paper-title">Inter-document Contextual Language model. </span><em>Quan Hung Tran, Ingrid Zukerman and Gholamreza Haffari</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-5b">
        <div id="expander"></div><a href="#" class="session-title">Sentiment</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ellen Riloff</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">Ultradense Word Embeddings by Orthogonal Transformation. </span><em>Sascha Rothe, Sebastian Ebert and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td>
                        <span class="paper-title">Separating Actor-View from Speaker-View Opinion Expressions using Linguistic Features. </span><em>Michael Wiegand, Marc Schulder and Josef Ruppenhofer</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td>
                        <span class="paper-title">Clustering for Simultaneous Extraction of Aspects and Features from Reviews. </span><em>Lu Chen, Justin Martineau, Doreen Cheng and Amit Sheth</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:20</td>
                    <td>
                        <span class="paper-title">Opinion Holder and Target Extraction on Opinion Compounds -- A Linguistic Approach. </span><em>Michael Wiegand, Christine Bocionek and Josef Ruppenhofer</em>
                    </td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td>
                        <span class="paper-title">Capturing Reliable Fine-Grained Sentiment Associations by Crowdsourcing and Best–Worst Scaling. </span><em>Svetlana Kiritchenko and Saif Mohammad</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-5c">
        <div id="expander"></div><a href="#" class="session-title">Knowledge Acquisition</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ray Mooney</td>
                </tr>
                <tr>
                    <td>11:00–11:20</td>
                    <td>
                        <span class="paper-title">Concept Grounding to Multiple Knowledge Bases via Indirect Supervision. </span><em>Chen-Tse Tsai and Dan Roth</em>
                    </td>
                </tr>
                <tr>
                    <td>11:20–11:40</td>
                    <td>
                        <span class="paper-title">Mapping Verbs in Different Languages to Knowledge Base Relations using Web Text as Interlingua. </span><em>Derry Tanti Wijaya and Tom Mitchell</em>
                    </td>
                </tr>
                <tr>
                    <td>11:40–12:00</td>
                    <td>
                        <span class="paper-title">Comparing Convolutional Neural Networks to Traditional Models for Slot Filling. </span><em>Heike Adel, Benjamin Roth and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr>
                    <td>12:00–12:20</td>
                    <td>
                        <span class="paper-title">A Corpus and Cloze Evaluation for Deeper Understanding of Commonsense Stories. </span><em>Nasrin Mostafazadeh, Nathanael Chambers, Xiaodong He, Devi Parikh, Dhruv Batra, Lucy Vanderwende, Pushmeet Kohli and James Allen</em>
                    </td>
                </tr>
                <tr>
                    <td>12:20–12:30</td>
                    <td>
                        <span class="paper-title">Dynamic Entity Representation with Max-pooling Improves Machine Reading. </span><em>Sosuke Kobayashi, Ran Tian, Naoaki Okazaki and Kentaro Inui</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 1:15 PM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-deep-learning-panel">
        <div id="expander"></div><a href="#" class="session-title">Panel Discussion: How Will Deep Learning Change Computational Linguistics?</a><br/>        
        <span class="session-time">1:15 PM &ndash; 2:15 PM</span><br/>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <strong>Moderator</strong>: Jason Eisner<br/>

                <strong>Panelists</strong>: Kyunghyun Cho, Chris Dyer, Pascale Fung, Heng Ji<br/>

                <ul>
                    <li>What are the big problems in NLP historically, now, and in the future? (What do we need to solve, regardless of the approach for solving it?)</li>
                    <li>What current NLP problems has DL solved, or where has DL made an important contribution towards improving the state of the art?</li>
                    <li>Does DL guide NLP towards new problems? Do we already have examples? Do you want to speculate? (Have a new hammer, looking for un-hammered nails.)</li>
                    <li>Does DL change our methodology profoundly, or is it just another machine learning method? Is there a greater danger of overfitting because of the massive tuning required? Given the computational requirements, are off-the-shelf tools incorporating DL practical?</li>
                    <li>Is the use of off-the-shelf word embeddings the major contribution of DL? Does every task in which in the past we had bag of words features now required to also use word embedding features?</li>
                    <li>Is linguistics obsolete because DL will find better representations on its own? Or should DL be combined with traditional representations of latent linguistic structure? What is the best way to do that – hybrid architectures, hybrid training objectives, hand-designed input representations, or something else?</li>
                    <li>Is DL mostly good for supervised mapping of input to output where very large training sets are available? Or can it also help for semi-supervised learning and unsupervised structure discovery?</li>
                    <li>What are the best approaches to interpretability (explaining why a DL system made a particular decision)? What are the best approaches to understanding the latent representations and figuring out what the system is missing and how to fix that?</li>
                    <li>How much do architectures and parameters need to be task-specific? How much can researchers reuse architectures, and learning algorithms reuse parameters, across tasks?</li>
                    <li>A DL design that looks nice on paper often doesn't work right away. What are best practices for achieving good performance? Do experienced researchers not have this problem because they know more tricks of the trade and have better intuitions about hyperparameters? Or does every paper involve 6 months of fiddling around on a dev set until it works? Is it worth doing automatic tuning of hyperparameters, e.g., Bayesian optimization? </li>
                </ul>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-papers1" id="session-6a">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation II</a><br/>
        <span class="session-time">2:30 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Colin Cherry</td>
                </tr>
                <tr>
                    <td>2:30–2:50</td>
                    <td>
                        <span class="paper-title">Speed-Constrained Tuning for Statistical Machine Translation Using Bayesian Optimization. </span><em>Daniel Beck, Adrià de Gispert, Gonzalo Iglesias, Aurelien Waite and Bill Byrne</em>
                    </td>
                </tr>
                <tr>
                    <td>2:50–3:10</td>
                    <td>
                        <span class="paper-title">Multi-Way, Multilingual Neural Machine Translation with a Shared Attention Mechanism. </span><em>Orhan Firat, Kyunghyun Cho and Yoshua Bengio</em>
                    </td>
                </tr>
                <tr>
                    <td>3:10–3:30</td>
                    <td>
                        <span class="paper-title">Incorporating Structural Alignment Biases into an Attentional Neural Translation Model. </span><em>Trevor Cohn, Cong Duy Vu Hoang, Ekaterina Vymolova, Kaisheng Yao, Chris Dyer and Gholamreza Haffari</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-6b">
        <div id="expander"></div><a href="#" class="session-title">Relation Extraction</a><br/>
        <span class="session-time">2:30 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Byron Wallace</td>
                </tr>
                <tr>
                    <td>2:30–2:50</td>
                    <td>
                        <span class="paper-title">Multilingual Relation Extraction using Compositional Universal Schema. </span><em>Patrick Verga, David Belanger, Emma Strubell, Benjamin Roth and Andrew McCallum</em>
                    </td>
                </tr>
                <tr>
                    <td>2:50–3:10</td>
                    <td>
                        <span class="paper-title">Effective Crowd Annotation for Relation Extraction. </span><em>Angli Liu, Stephen Soderland, Jonathan Bragg, Christopher Lin, Xiao Ling and Daniel Weld</em>
                    </td>
                </tr>
                <tr>
                    <td>3:10–3:30</td>
                    <td>
                        <span class="paper-title">A Translation-Based Knowledge Graph Embedding Preserving Logical Property of Relations. </span><em>Hee-Geun Yoon, Hyun-Je Song, Seong-Bae Park and Se-Young Park</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-6c">
        <div id="expander"></div><a href="#" class="session-title">Semantic Similarity</a><br/>
        <span class="session-time">2:30 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Dipanjan Das</td>
                </tr>
                <tr>
                    <td>2:30–2:50</td>
                    <td>
                        <span class="paper-title">DAG-Structured Long Short-Term Memory for Semantic Compositionality. </span><em>Xiaodan Zhu, Parinaz Sobhani and Hongyu Guo</em>
                    </td>
                </tr>
                <tr>
                    <td>2:50–3:10</td>
                    <td>
                        <span class="paper-title">Bayesian Supervised Domain Adaptation for Short Text Similarity. </span><em>Md Arafat Sultan, Jordan Boyd-Graber and Tamara Sumner</em>
                    </td>
                </tr>
                <tr>
                    <td>3:10–3:30</td>
                    <td>
                        <span class="paper-title">Pairwise Word Interaction Modeling with Deep Neural Networks for Semantic Similarity Measurement. </span><em>Hua He and Jimmy Lin</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:30 PM &ndash; 4:00 PM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-7a">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation III</a><br/>
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Marine Carpuat</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">An Attentional Model for Speech Translation Without Transcription. </span><em>Long Duong, Antonios Anastasopoulos, David Chiang, Steven Bird and Trevor Cohn</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">Information Density and Quality Estimation Features as Translationese Indicators for Human Translation Classification. </span><em>Raphael Rubino, Ekaterina Lapshinova-Koltunski and Josef van Genabith</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–4:50</td>
                    <td>
                        <span class="paper-title">Interpretese vs. Translationese: The Uniqueness of Human Strategies in Simultaneous Interpretation. </span><em>He He, Jordan Boyd-Graber and Hal Daumé III</em>
                    </td>
                </tr>
                <tr>
                    <td>4:50–5:00</td>
                    <td>
                        <span class="paper-title">LSTM Neural Reordering Feature for Statistical Machine Translation. </span><em>Yiming Cui, Shijin Wang and Jianfeng Li</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-7b">
        <div id="expander"></div><a href="#" class="session-title">Anaphora Resolution</a><br/>
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Vincent Ng</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">A Novel Approach to Dropped Pronoun Translation. </span><em>Longyue Wang, Zhaopeng Tu, Xiaojun Zhang, Hang Li, Andy Way and Qun Liu</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">Learning Global Features for Coreference Resolution. </span><em>Sam Wiseman, Alexander M. Rush and Stuart Shieber</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–4:50</td>
                    <td>
                        <span class="paper-title">Search Space Pruning: A Simple Solution for Better Coreference Resolvers. </span><em>Nafise Sadat Moosavi and Michael Strube</em>
                    </td>
                </tr>
                <tr>
                    <td>4:50–5:00</td>
                    <td>
                        <span class="paper-title">Unsupervised Ranking Model for Entity Coreference Resolution. </span><em>Xuezhe Ma, Zhengzhong Liu and Eduard Hovy</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-7c">
        <div id="expander"></div><a href="#" class="session-title">Word Embeddings I</a><br/>
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Manaal Faruqui</td>
                </tr>
                <tr>
                    <td>4:00–4:20</td>
                    <td>
                        <span class="paper-title">Embedding Lexical Features via Low-Rank Tensors. </span><em>Mo Yu, Mark Dredze, Raman Arora and Matthew R. Gormley</em>
                    </td>
                </tr>
                <tr>
                    <td>4:20–4:40</td>
                    <td>
                        <span class="paper-title">The Role of Context Types and Dimensionality in Learning Word Embeddings. </span><em>Oren Melamud, David McClosky, Siddharth Patwardhan and Mohit Bansal</em>
                    </td>
                </tr>
                <tr>
                    <td>4:40–5:00</td>
                    <td>
                        <span class="paper-title">Improve Chinese Word Embeddings by Exploiting Internal Structure. </span><em>Jian Xu, Jiawei Liu, Liangang Zhang, Zhengyu Li and Huanhuan Chen</em>
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
        <span class="session-time">5:15 PM &ndash; 6:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Chair: Joel Tetreault</p>

                <p>Prior to the poster session, TACL and long-paper poster presenters will be given one minute each to pitch their paper. The poster session will immediately follow these presentations along with a buffet dinner.</p>
            </div>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-second-poster">
        <div id="expander"></div><a href="#" class="session-title">Posters, Demos &amp; Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
        <span class="session-location btn btn--location">Pavilion</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <span class="info-button btn btn--small">Main Conference</span>
            <table class="paper-table">
                <tr>
                    <td>
                        <span class="paper-title">Assessing Relative Sentence Complexity using an Incremental CCG Parser. </span><em>Bharat Ram Ambati, Siva Reddy and Mark Steedman</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Automatic Prediction of Linguistic Decline in Writings of Subjects with Degenerative Dementia. </span><em>Davy Weissenbacher, Travis A. Johnson, Laura Wojtulewicz, Amylou Dueck, Dona Locke, Richard Caselli and Graciela Gonzalez</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Automatically Inferring Implicit Properties in Similes. </span><em>Ashequl Qadir, Ellen Riloff and Marilyn Walker</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">BIRA: Improved Predictive Exchange Word Clustering. </span><em>Jon Dehdari, Liling Tan and Josef van Genabith</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Bootstrapping Translation Detection and Sentence Extraction from Comparable Corpora. </span><em>Kriste Krstovski and David Smith</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Capturing Semantic Similarity for Entity Linking with Convolutional Neural Networks. </span><em>Matthew Francis-Landau, Greg Durrett and Dan Klein</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Consensus Maximization Fusion of Probabilistic Information Extractors. </span><em>Miguel Rodriguez, Sean Goldberg and Daisy Zhe Wang</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Cross-genre Event Extraction with Knowledge Enrichment. </span><em>Hao Li and Heng Ji</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Deep Lexical Segmentation and Syntactic Parsing in the Easy-First Dependency Framework. </span><em>Matthieu Constant, Joseph Le Roux and Nadi Tomeh</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Discriminative Reranking for Grammatical Error Correction with Statistical Machine Translation. </span><em>Tomoya Mizumoto and Yuji Matsumoto</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Emergent: a novel data-set for stance classification. </span><em>William Ferreira and Andreas Vlachos</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Eyes Don't Lie: Predicting Machine Translation Quality Using Eye Movement. </span><em>Hassan Sajjad, Francisco Guzmán, Nadir Durrani, Ahmed Abdelali, Houda Bouamor, Irina Temnikova and Stephan Vogel</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Fast and Easy Short Answer Grading with High Accuracy. </span><em>Md Arafat Sultan, Cristobal Salazar and Tamara Sumner</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Frustratingly Easy Cross-Lingual Transfer for Transition-Based Dependency Parsing. </span><em>Ophélie Lacroix, Lauriane Aufrant, Guillaume Wisniewski and François Yvon</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Geolocation for Twitter: Timing Matters. </span><em>Mark Dredze, Miles Osborne and Prabhanjan Kambadur</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Incorporating Side Information into Recurrent Neural Network Language Models. </span><em>Cong Duy Vu Hoang, Trevor Cohn and Gholamreza Haffari</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Integrating Morphological Desegmentation into Phrase-based Decoding. </span><em>Mohammad Salameh, Colin Cherry and Grzegorz Kondrak</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Interlocking Phrases in Phrase-based Statistical Machine Translation. </span><em>Ye Kyaw Thu, Andrew Finch and Eiichiro Sumita</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">K-Embeddings: Learning Conceptual Embeddings for Words using Context. </span><em>Thuy Vu and D. Stott Parker</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Learning Composition Models for Phrase Embeddings. </span><em>Mo Yu and Mark Dredze</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Learning a POS tagger for AAVE-like language. </span><em>Anna Jørgensen, Dirk Hovy and Anders Søgaard</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Learning to Recognize Ancillary Information for Automatic Paraphrase Identification. </span><em>Simone Filice and Alessandro Moschitti</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">MAWPS: A Math Word Problem Repository. </span><em>Rik Koncel-Kedziorski, Subhro Roy, Aida Amini, Nate Kushman and Hannaneh Hajishirzi</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Making Dependency Labeling Simple, Fast and Accurate. </span><em>Tianxiao Shen, Tao Lei and Regina Barzilay</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">PIC a Different Word: A Simple Model for Lexical Substitution in Context. </span><em>Stephen Roller and Katrin Erk</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">PRIMT: A Pick-Revise Framework for Interactive Machine Translation. </span><em>Shanbo Cheng, Shujian Huang, Huadong Chen, Xin-Yu Dai and Jiajun Chen</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Patterns of Wisdom: Discourse-Level Style in Multi-Sentence Quotations. </span><em>Kyle Booten and Marti A. Hearst</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Right-truncatable Neural Word Embeddings. </span><em>Jun Suzuki and Masaaki Nagata</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Sentiment Composition of Words with Opposing Polarities. </span><em>Svetlana Kiritchenko and Saif Mohammad</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Simple, Fast Noise-Contrastive Estimation for Large RNN Vocabularies. </span><em>Barret Zoph, Ashish Vaswani, Jonathan May and Kevin Knight</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Sparse Bilingual Word Representations for Cross-lingual Lexical Entailment. </span><em>Yogarshi Vyas and Marine Carpuat</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">The Instantiation Discourse Relation: A Corpus Analysis of Its Properties and Improved Detection. </span><em>Junyi Jessy Li and Ani Nenkova</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Visual Storytelling. </span><em>Ting-Hao Huang, Francis Ferraro, Nasrin Mostafazadeh, Ishan Misra, Jacob Devlin, Aishwarya Agrawal, Ross Girshick, Xiaodong He, Pushmeet Kohli, Dhruv Batra, Larry Zitnick, Devi Parikh, Lucy Vanderwende, Michel Galley and Margaret Mitchell</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small">Student Research Workshop</span>
            <table class="paper-table">
                <tr>
                    <td>
                        <span class="paper-title">Effects of Communicative Pressures on Novice L2 Learners' Use of Optional Formal Devices. </span><em>Yoav Binoun, Francesca Delogu, Clayton Greenberg, Mindaugas Mozuraitis and Matthew Crocker</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Explicit Argument Identification for Discourse Parsing In Hindi: A Hybrid Pipeline. </span><em>Rohit Jain and Dipti Sharma</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Exploring Fine-Grained Emotion Detection in Tweets. </span><em>Jasy Suet Yan Liew and Howard Turtle</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Extraction of Bilingual Technical Terms for Chinese-Japanese Patent Translation. </span><em>Wei Yang, Jinghui Yan and Yves Lepage</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter. </span><em>Zeerak Waseem and Dirk Hovy</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Non-decreasing Sub-modular Function for Comprehensible Summarization. </span><em>Litton JKurisinkel, Pruthwik Mishra, Vigneshwaran Muralidaran, Vasudeva Varma and Dipti Misra Sharma</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Phylogenetic simulations over constraint-based grammar formalisms. </span><em>Andrew Lamont and Jonathan Washington</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Question Answering over Knowledge Base using Weakly Supervised Memory Networks. </span><em>Sarthak Jain</em>
                    </td>
                </tr>
                <tr>
                    <td>
                        <span class="paper-title">Using Related Languages to Enhance Statistical Language Models. </span><em>Anna Currey, Alina Karakanta and Jon Dehdari</em>
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
        <span class="session-location btn btn--location">Bayview Lawn</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                
                <span class="info-button btn btn--small">Included in registration</span>

                <p>Enjoy a fun evening under the stars!</p>

                <p>Bring your Flower Power to our SoCal Beach Party! After the main dinner and Poster Session, join us on the Bayview Lawn adjacent to the Pavilion for desserts, coffee, tea, and drinks (cash bar). A Beach Boys style band will entertain you when you are not busy in the VW Bus Photo Booth, talking amongst your friends and colleagues, or playing with the beach balls.</p>

                <p>Learn more about the social event <a class="info-link" target="_blank" href="http://naacl.org/naacl-hlt-2016/social_event.html">here</a>.</p>
            </div>
        </div>
    </div>
    <div class="day" id="fourth-day">Wednesday, June 15</div>
    <div class="session session-plenary">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-invited-ehud">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: Evaluating Natural Language Generation Systems</a><br/>
        <span class="session-people">Ehud Reiter</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:15 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Natural Language Generation (NLG) systems have different characteristics than other NLP systems, which effects how they are evaluated. In particular, it can be difficult to meaningfully evaluate NLG texts by comparing them against gold-standard reference texts, because (A) there are usually many possible texts which are acceptable to users and (B) some NLG systems produce texts which are better (as judged by human users) than human-written corpus texts. Partially because of these reasons, the NLG community places much more emphasis on human-based evaluations than most areas of NLP.</p>

                <p>I will discuss the various ways in which NLG systems are evaluated, focusing on human-based evaluations. These typically either measure the success of generated texts at achieving a goal (eg, measuring how many people change their behaviour after reading behaviour-change texts produced by an NLG system); or ask human subjects to rate various aspects of generated texts (such as readability, accuracy, and appropriateness), often on Likert scales. I will use examples from evaluations I have carried out, and highlight some of the lessons I have learnt, including the importance of reporting negative results, the difference between laboratory and real-world evaluations, and the need to look at worse-case as well as average-case performance. I hope my talk will be interesting and relevant to anyone who is interested in the evaluation of NLP systems.</p>
            </div>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:15 AM &ndash; 10:45 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-8a">
        <div id="expander"></div><a href="#" class="session-title">Question Answering</a><br/>
        <span class="session-time">10:45 AM &ndash; 12:15 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ed Hovy</td>
                </tr>
                <tr>
                    <td>10:45–11:05</td>
                    <td>
                        <span class="paper-title">A Joint Model for Answer Sentence Ranking and Answer Extraction. </span><em>Md Arafat Sultan, Vittorio Castelli and Radu Florian</em>
                    </td>
                </tr>
                <tr>
                    <td>11:05–11:25</td>
                    <td>
                        <span class="paper-title">Convolutional Neural Networks vs. Convolution Kernels: Feature Engineering for Answer Sentence Reranking. </span><em>Kateryna Tymoshenko, Daniele Bonadiman and Alessandro Moschitti</em>
                    </td>
                </tr>
                <tr>
                    <td>11:25–11:45</td>
                    <td>
                        <span class="paper-title">Semi-supervised Question Retrieval with Gated Convolutions. </span><em>Tao Lei, Hrishikesh Joshi, Regina Barzilay, Tommi Jaakkola, Kateryna Tymoshenko, Alessandro Moschitti and Lluís Màrquez</em>
                    </td>
                </tr>
                <tr>
                    <td>11:45–12:05</td>
                    <td>
                        <span class="paper-title">Parsing Algebraic Word Problems into Equations. </span><em>Rik Koncel-Kedziorski, Hannaneh Hajishirzi, Ashish Sabharwal, Oren Etzioni and Siena Dumas Ang</em>
                    </td>
                </tr>
                <tr>
                    <td>12:05–12:15</td>
                    <td>
                        <span class="paper-title">This is how we do it: Answer Reranking for Open-domain How Questions with Paragraph Vectors and Minimal Feature Engineering. </span><em>Dasha Bogdanova and Jennifer Foster</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-8b">
        <div id="expander"></div><a href="#" class="session-title">Multilingual Processing</a><br/>
        <span class="session-time">10:45 AM &ndash; 12:15 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mohit Bansal</td>
                </tr>
                <tr>
                    <td>10:45–11:05</td>
                    <td>
                        <span class="paper-title">Multilingual Language Processing From Bytes. </span><em>Daniel Gillick, Cliff Brunk, Oriol Vinyals and Amarnag Subramanya</em>
                    </td>
                </tr>
                <tr>
                    <td>11:05–11:25</td>
                    <td>
                        <span class="paper-title">Ten Pairs to Tag -- Multilingual POS Tagging via Coarse Mapping between Embeddings. </span><em>Yuan Zhang, David Gaddy, Regina Barzilay and Tommi Jaakkola</em>
                    </td>
                </tr>
                <tr>
                    <td>11:25–11:45</td>
                    <td>
                        <span class="paper-title">Part-of-Speech Tagging for Historical English. </span><em>Yi Yang and Jacob Eisenstein</em>
                    </td>
                </tr>
                <tr>
                    <td>11:45–12:05</td>
                    <td>
                        <span class="paper-title">Statistical Modeling of Creole Genesis. </span><em>Yugo Murawaki</em>
                    </td>
                </tr>
                <tr>
                    <td>12:05–12:15</td>
                    <td>
                        <span class="paper-title">Shallow Parsing Pipeline - Hindi-English Code-Mixed Social Media Text. </span><em>Arnav Sharma, Sakshi Gupta, Raveesh Motlani, Piyush Bansal, Manish Shrivastava, Radhika Mamidi and Dipti Sharma</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-8c">
        <div id="expander"></div><a href="#" class="session-title">Word Embeddings II</a><br/>
        <span class="session-time">10:45 AM &ndash; 12:15 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Hinrich Schütze</td>
                </tr>
                <tr>
                    <td>10:45–11:05</td>
                    <td>
                        <span class="paper-title">Bilingual Learning of Multi-sense Embeddings with Discrete Autoencoders. </span><em>Simon Suster, Ivan Titov and Gertjan van Noord</em>
                    </td>
                </tr>
                <tr>
                    <td>11:05–11:25</td>
                    <td>
                        <span class="paper-title">Polyglot Neural Language Models: A Case Study in Cross-Lingual Phonetic Representation Learning. </span><em>Yulia Tsvetkov, Sunayana Sitaram, Manaal Faruqui, Guillaume Lample, Patrick Littell, David R. Mortensen, Alan W Black, Lori Levin and Chris Dyer</em>
                    </td>
                </tr>
                <tr>
                    <td>11:25–11:45</td>
                    <td>
                        <span class="paper-title">Learning Distributed Representations of Sentences from Unlabelled Data. </span><em>Felix Hill, Kyunghyun Cho and Anna Korhonen</em>
                    </td>
                </tr>
                <tr>
                    <td>11:45–12:05</td>
                    <td>
                        <span class="paper-title">Learning to Understand Phrases by Embedding the Dictionary. </span><em>Felix Hill, Kyunghyun Cho, Anna Korhonen and Yoshua Bengio</em>
                    </td>
                </tr>
                <tr>
                    <td>12:05–12:15</td>
                    <td>
                        <span class="paper-title">Retrofitting Sense-Specific Word Vectors Using Parallel Text. </span><em>Allyson Ettinger, Philip Resnik and Marine Carpuat</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:15 PM &ndash; 1:00 PM</span>
    </div>
    <div class="session session-plenary" id="session-business-meeting">
        <a href="#" class="session-title">NAACL Business Meeting</a><br/>
        <span class="session-people"><strong>All attendees are encouraged to participate in the business meeting.</strong></span><br/>
        <span class="session-time">1:00 PM &ndash; 2:00 PM</span><br/>
    </div>
    <div class="session session-expandable session-papers1" id="session-9a">
        <div id="expander"></div><a href="#" class="session-title">Argumentation &amp; Discourse Relations</a><br/>
        <span class="session-time">2:15 PM &ndash; 3:45 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Cristian Danescu-Niculescu-Mizil</td>
                </tr>
                <tr>
                    <td>2:15–2:35</td>
                    <td>
                        <span class="paper-title">End-to-End Argumentation Mining in Student Essays. </span><em>Isaac Persing and Vincent Ng</em>
                    </td>
                </tr>
                <tr>
                    <td>2:35–2:55</td>
                    <td>
                        <span class="paper-title">Cross-Domain Mining of Argumentative Text through Distant Supervision. </span><em>Khalid Al Khatib, Henning Wachsmuth, Matthias Hagen, Jonas Köhler and Benno Stein</em>
                    </td>
                </tr>
                <tr>
                    <td>2:55–3:15</td>
                    <td>
                        <span class="paper-title">A Study of the Impact of Persuasive Argumentation in Political Debates. </span><em>Amparo Elizabeth Cano Basave and Yulan Hu</em>
                    </td>
                </tr>
                <tr>
                    <td>3:15–3:35</td>
                    <td>
                        <span class="paper-title">Lexical Coherence Graph Modeling Using Word Embeddings. </span><em>Mohsen Mesgar and Michael Strube</em>
                    </td>
                </tr>
                <tr>
                    <td>3:35–3:45</td>
                    <td>
                        <span class="paper-title">Using Context to Predict the Purpose of Argumentative Writing Revisions. </span><em>Fan Zhang and Diane Litman</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-9b">
        <div id="expander"></div><a href="#" class="session-title">Misc. Semantics</a><br/>
        <span class="session-time">2:15 PM &ndash; 3:45 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom B</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Steven Bethard</td>
                </tr>
                <tr>
                    <td>2:15–2:35</td>
                    <td>
                        <span class="paper-title">Automatic Generation and Scoring of Positive Interpretations from Negated Statements. </span><em>Eduardo Blanco and Zahra Sarabi</em>
                    </td>
                </tr>
                <tr>
                    <td>2:35–2:55</td>
                    <td>
                        <span class="paper-title">Learning Natural Language Inference with LSTM. </span><em>Shuohang Wang and Jing Jiang</em>
                    </td>
                </tr>
                <tr>
                    <td>2:55–3:15</td>
                    <td>
                        <span class="paper-title">Activity Modeling in Email. </span><em>Ashequl Qadir, Michael Gamon, Patrick Pantel and Ahmed Awadallah</em>
                    </td>
                </tr>
                <tr>
                    <td>3:15–3:35</td>
                    <td>
                        <span class="paper-title">Clustering Paraphrases by Word Sense. </span><em>Anne Cocos and Chris Callison-Burch</em>
                    </td>
                </tr>
                <tr>
                    <td>3:35–3:45</td>
                    <td>
                        <span class="paper-title">Unsupervised Learning of Prototypical Fillers for Implicit Semantic Role Labeling. </span><em>Niko Schenk and Christian Chiarcos</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-9c">
        <div id="expander"></div><a href="#" class="session-title">Text Categorization</a><br/>
        <span class="session-time">2:15 PM &ndash; 3:45 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom C</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Jacob Eisenstein</td>
                </tr>
                <tr>
                    <td>2:15–2:35</td>
                    <td>
                        <span class="paper-title">Hierarchical Attention Networks for Document Classification. </span><em>Zichao Yang, Diyi Yang, Chris Dyer, Xiaodong He, Alex Smola and Eduard Hovy</em>
                    </td>
                </tr>
                <tr>
                    <td>2:35–2:55</td>
                    <td>
                        <span class="paper-title">Dependency Based Embeddings for Sentence Classification Tasks. </span><em>Alexandros Komninos and Suresh Manandhar</em>
                    </td>
                </tr>
                <tr>
                    <td>2:55–3:15</td>
                    <td>
                        <span class="paper-title">Deep LSTM based Feature Mapping for Query Classification. </span><em>Yangyang Shi, Kaisheng Yao, Le Tian and Daxin Jiang</em>
                    </td>
                </tr>
                <tr>
                    <td>3:15–3:35</td>
                    <td>
                        <span class="paper-title">Dependency Sensitive Convolutional Neural Networks for Modeling Sentences and Documents. </span><em>Rui Zhang, Honglak Lee and Dragomir Radev</em>
                    </td>
                </tr>
                <tr>
                    <td>3:35–3:45</td>
                    <td>
                        <span class="paper-title">MGNC-CNN: A Simple Approach to Exploiting Multiple Word Embeddings for Sentence Classification. </span><em>Ye Zhang, Stephen Roller and Byron C. Wallace</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:45 PM &ndash; 4:15 PM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-best-papers">
        <div id="expander"></div><a href="#" class="session-title">Best Papers Presentation</a><br/>        
        <span class="session-time">4:15 PM &ndash; 5:45 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom</span><br/>
        <div class="paper-session-details">
            <hr class="detail-separator"/>            
            <div class="session-abstract"><p>Chair: Owen Rambow</p></div>

            <span class="info-button btn btn--small">Best Short Paper</span>
            <table class="paper-table">
                <tr>
                    <td>4:15–4:35</td>
                    <td>
                    <span class="paper-title">Improving sentence compression by learning to predict gaze. </span><em>Sigrid Klerke, Yoav Goldberg and Anders Søgaard</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small">Best Long Papers</span>
            <table class="paper-table">
                <tr>
                    <td>4:35–5:05</td>
                    <td>
                        <span class="paper-title">Feuding Families and Former Friends; Unsupervised Learning for Dynamic Fictional Relationships. </span><em>Mohit Iyyer, Anupam Guha, Snigdha Chaturvedi, Jordan Boyd-Graber and Hal Daumé III</em>
                    </td>
                </tr>
                <tr>
                    <td>5:05–5:35</td>
                    <td>
                        <span class="paper-title">Learning to Compose Neural Networks for Question Answering. </span><em>Jacob Andreas, Marcus Rohrbach, Trevor Darrell and Dan Klein</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary">
        <span class="session-title">Closing Remarks</span><br/>        
        <span class="session-time">5:35 PM &ndash; 5:45 PM</span>
    </div>

</div>

