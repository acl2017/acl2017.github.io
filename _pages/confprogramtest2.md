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
                    <span class="paper-title">[T1] English Resource Semantics</span><br/>
                    <a href="#" class="btn btn--location inline-location">Executive 3AB</a>
                </li>
                <li>
                 <span class="paper-title">[T2] Multilingual Multimodal Language Processing Using Neural Networks</span><br/>
                 <a href="#" class="btn btn--location inline-location">Spinnaker</a>
             </li>
             <li>
                <span class="paper-title">[T3] Question Answering with Knowledge Base, Web and Beyond</span><br/>
                <a href="#" class="btn btn--location inline-location">Marina 3</a></li>
            </ul>      
        </div>
    </div>
    <div class="session session-tutorials">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 2:00 PM</span>
    </div>
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials">
        <a href="#" class="session-title">Afternoon Tutorials</a><br/>        
        <span class="session-time">2:00 PM &ndash; 5:00 PM</span>
        <div class="session-details">
            <ul>
                <li>
                    <span class="paper-title">[T4] Recent Progress in Deep Learning for NLP</span><br/>
                    <a href="#" class="btn btn--location inline-location">Spinnaker</a>
                </li>
                <li>
                 <span class="paper-title">[T5] Scalable Statistical Relational Learning for NLP</span><br/>
                 <a href="#" class="btn btn--location inline-location">Marina 3</a>
             </li>
             <li>
                <span class="paper-title">[T6] Statistical Machine Translation between Related Languages</span><br/>
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
    <div class="session session-expandable session-papers1" id="session-1a">
        <a href="#" class="session-title">Machine Translation I</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <div class="session-details">
        foobar
        </div> 
    </div>
    <div class="session session-expandable session-papers2" id="session-1b">
        <a href="#" class="session-title">Machine Translation I</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <div class="session-details">
        foobar
        </div> 
    </div>
    <div class="session session-expandable session-papers3" id="session-1c">
        <a href="#" class="session-title">Machine Translation I</a><br/>        
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <div class="session-details">
        foobar
        </div> 
    </div>
</div>
