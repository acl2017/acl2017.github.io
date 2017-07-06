---
title: Conference Program
layout: schedule
excerpt: "ACL 2017 conference program."
permalink: /testing/program
sidebar: false
script: |
    <script>vex.defaultOptions.className = 'vex-theme-wireframe'</script>
    <script type="text/javascript">

        sessionInfoHash = {};
        paperInfoHash = {};
        chosenPapersHash = {};
        chosenTutorialsHash = {};
        chosenPostersHash = {};
        plenarySessionHash = {};
        includePlenaryInSchedule = true;

        function padTime(str) {
            return String('0' + str).slice(-2);
        }

        function formatDate(dateObj) {
            return dateObj.toLocaleDateString() + ' ' + padTime(dateObj.getHours()) + ':' + padTime(dateObj.getMinutes());
        }

        function inferAMPM(time) {
            var hour = time.split(':')[0];
            return (hour == 12 || hour <= 6) ? ' PM' : ' AM';
        }

        function generatePDFfromTable() {

            /* clear the hidden table before starting */
            clearHiddenProgramTable();

            /* now populate the hidden table with the currently chosen papers */
            populateHiddenProgramTable();

            var doc = new jsPDF('l', 'pt', 'letter');
            doc.autoTable({
                fromHtml: "#hidden-program-table",
                pagebreak: 'avoid',
                avoidRowSplit: true,
                theme: 'grid',
                startY: 70, 
                showHead: false,
                styles: {
                    font: 'times',
                    overflow: 'linebreak',
                    valign: 'middle',
                    lineWidth: 0.4,
                    fontSize: 11
                },
                 columnStyles: {
                    0: { fontStyle: 'bold', halign: 'right', cellWidth: 70 },
                    1: { cellWidth: 110 },
                    2: { fontStyle: 'italic', cellWidth: 530 }
                },
                addPageContent: function (data) {
                    /* HEADER only on the first page */
                    var pageNumber = doc.internal.getCurrentPageInfo().pageNumber;

                    if (pageNumber == 1) {
                        doc.setFontSize(16);
                        doc.setFontStyle('normal');
                        doc.text("ACL 2017 Schedule", (doc.internal.pageSize.width - (data.settings.margin.left*2))/2 - 30, 50);
                    }

                    /* FOOTER on each page */
                    doc.setFont('courier');
                    doc.setFontSize(8);
                    doc.text('(Generated via http://acl2017.org/testing/program)', data.settings.margin.left, doc.internal.pageSize.height - 10);
                },
                drawCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    /* center the day header */
                    if (cellClass == 'info-day') {
                        cell.textPos.x = (530 - data.settings.margin.left)/2 + 120;
                    }
                    /* split long plenary session text */
                    else if (cellClass == 'info-plenary') {
                        cell.text = doc.splitTextToSize(cell.text.join(' '), 530, {fontSize: 11});
                    }
                },
                createdCell: function(cell, data) {
                    var cellClass = cell.raw.content.className;
                    var cellText = cell.text[0];
                    /* */
                    if (cellClass == 'info-day') {
                        cell.styles.fontStyle = 'bold';
                        cell.styles.fontSize = 12;
                        cell.styles.fillColor = [187, 187, 187];
                    }
                    else if (cellClass == 'info-plenary') {
                        cell.styles.fontSize = 11;
                        if (cellText == "Break" || cellText == "Lunch" || cellText == "Breakfast") {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                    else if (cellClass == 'info-poster') {
                        cell.styles.fontSize = 9;
                    }
                    else if (cellClass == "location") {
                        if (cellText == '') {
                            var infoType = data.row.raw[2].content.className;
                            if (infoType == "info-day") {
                                cell.styles.fillColor = [187, 187, 187];
                            }
                            else if (infoType == "info-plenary") {
                                cell.styles.fillColor = [238, 238, 238];
                            }
                        }
                    }
                    else if (cellClass == "time") {
                        var infoType = data.row.raw[2].content.className;
                        var infoText = data.row.raw[2].content.textContent;
                        if (infoType == "info-day" && cellText == '') {
                            cell.styles.fillColor = [187, 187, 187];
                        }
                        if (infoType == "info-plenary" && (infoText == "Break" || infoText == "Lunch" || infoText == "Breakfast")) {
                            cell.styles.fillColor = [238, 238, 238];
                        }
                    }
                },
            });
            doc.output('dataurlnewwindow');
        }

        function getTutorialInfoFromTime(tutorialTimeObj) {

            /* get the tutorial session and day */
            var tutorialSession = tutorialTimeObj.parents('.session');
            var sessionDay = tutorialSession.prevAll('.day:first').text().trim();

            /* get the tutorial slot and the starting and ending times */
            var tutorialTimeText = tutorialTimeObj.text().trim();
            var tutorialTimes = tutorialTimeText.split(' ');
            var tutorialSlotStart = tutorialTimes[0];
            var tutorialSlotEnd = tutorialTimes[3];
            var tutorialSlotAMPM = inferAMPM(tutorialSlotStart);
            var exactTutorialStartingTime = sessionDay + ', 2017 ' + tutorialSlotStart + tutorialSlotAMPM;
            return [new Date(exactTutorialStartingTime).getTime(), tutorialSlotStart, tutorialSlotEnd, tutorialSession.attr('id')];
        }

        function getPosterInfoFromTime(posterTimeObj) {

            /* get the poster session and day */
            var posterSession = posterTimeObj.parents('.session');
            var sessionDay = posterSession.prevAll('.day:first').text().trim();

            /* get the poster slot and the starting and ending times */
            var posterTimeText = posterTimeObj.text().trim();
            var posterTimes = posterTimeText.split(' ');
            var posterSlotStart = posterTimes[0];
            var posterSlotEnd = posterTimes[3];
            var posterSlotAMPM = inferAMPM(posterSlotStart);
            var exactPosterStartingTime = sessionDay + ', 2017 ' + posterSlotStart + posterSlotAMPM;
            return [new Date(exactPosterStartingTime).getTime(), posterSlotStart, posterSlotEnd, posterSession.attr('id')];
        }

        function isOverlapping(thisPaperRange, otherPaperRange) {
            var thisStart = thisPaperRange[0];
            var thisEnd = thisPaperRange[1];
            var otherStart = otherPaperRange[0];
            var otherEnd = otherPaperRange[1];
            return ((thisStart <= otherEnd) && (thisEnd >= otherStart));
        }

        function getConflicts(paperObject) {

            /* first get the parallel sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            var thisPaperRange = paperInfoHash[paperObject.attr('paper-id')].slice(0, 2);
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) {
                    var otherPaperRange =  paperInfoHash[$(this).attr('paper-id')].slice(0, 2);
                    return isOverlapping(thisPaperRange, otherPaperRange) 
                });
        }

        function getConflicts2(paperObject) {

            /* most of the time, conflicts are simply based on papers having the same exact time slot but this is not always true */

            /* first get the conflicting sessions */
            var sessionId = paperObject.parents('.session').attr('id').match(/session-\d/)[0];
            var parallelSessions = paperObject.parents('.session').siblings().filter(function() { return this.id.match(sessionId); });
            
            /* now get the conflicting papers from those sessions */
            var paperTime = paperObject.children('td#paper-time')[0].textContent;
            return $(parallelSessions).find('table.paper-table tr#paper').filter(function(index) { return this.children[0].textContent == paperTime });

        }

        function makeDayHeaderRow(day) {
            return '<tr><td class="time"></td><td class="location"></td><td class="info-day">' + day + '</td></tr>';
        }

        function makePlenarySessionHeaderRow(session) {
            var startWithoutAMPM = session.start.slice(0, -3);
            var endWithoutAMPM = session.end.slice(0, -3);
            return '<tr><td class="time">' + startWithoutAMPM + '&ndash;' + endWithoutAMPM + '</td><td class="location">' + session.location + '</td><td class="info-plenary">' + session.title + '</td></tr>';
        }

        function makePaperRows(start, end, titles, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + sessions[0].location + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    rows.push('<tr><td></td><td class="location">' + session.location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makeTutorialRows(start, end, titles, locations, sessions) {
            var ans;
            if (titles.length == 1) {
                ans = ['<tr><td class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
            }
            else {
                var numConflicts = titles.length;
                rows = ['<tr><td rowspan=' + numConflicts + ' class="time">' + start + '&ndash;' + end + '</td><td class="location">' + locations[0] + '</td><td class="info-paper">' + titles[0] + ' [' + sessions[0].title + ']</td></tr>'];
                for (var i=1; i<numConflicts; i++) {
                    var session = sessions[i];
                    var title = titles[i];
                    var location = locations[i];
                    rows.push('<tr><td></td><td class="location">' + location + '</td><td class="info-paper">' + title + ' [' + session.title + ']</td></tr>')
                }
                ans = rows;
            }
            return ans;
        }

        function makePosterRows(titles, types, sessions) {
            var numPosters = titles.length;
            var startWithoutAMPM = sessions[0].start.slice(0, -3);
            var endWithoutAMPM = sessions[0].end.slice(0, -3);
            rows = ['<tr><td rowspan=' + (numPosters + 1) + ' class="time">' + startWithoutAMPM + '&ndash;' + endWithoutAMPM + '</td><td rowspan=' + (numPosters + 1) + ' class="location">' + sessions[0].location + '</td><td class="info-paper">' + sessions[0].title +  '</td></tr>'];
            for (var i=0; i<numPosters; i++) {
                var title = titles[i];
                var type = types[i];
                rows.push('<tr><td></td><td></td><td class="info-poster">' + title + ' [' + type + ']</td></tr>');
            }
            return rows;
        }

        function clearHiddenProgramTable() {
            $('#hidden-program-table tbody').html('');
        }

        function getChosenHashFromType(type) {
            var chosenHash;
            if (type == 'paper') {
                chosenHash = chosenPapersHash;
            }
            else if (type == 'tutorial') {
                chosenHash = chosenTutorialsHash;
            }
            else if (type == 'poster') {
                chosenHash = chosenPostersHash;
            }
            return chosenHash;
        }

        function addToChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                items.push(item);
                chosenHash[timeKey] = items;
            }
            else {
                chosenHash[timeKey] = [item];
            }
        }

        function removeFromChosen(timeKey, item, type) {
            var chosenHash = getChosenHashFromType(type);            
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                if (itemIndex !== -1) {
                    var removedItem = items.splice(itemIndex, 1);
                    delete removedItem;
                    if (items.length == 0) {
                        delete chosenHash[timeKey];
                    }
                    else {
                        chosenHash[timeKey] = items;
                    }
                }
            }
        }

        function isChosen(timeKey, item, type) {
            var ans = false;
            var chosenHash = getChosenHashFromType(type);
            if (timeKey in chosenHash) {
                var items = chosenHash[timeKey];
                var itemIndex = items.map(function(item) { return item.title; }).indexOf(item.title);
                ans = itemIndex !== -1;
            }
            return ans;
        }

        function toggleSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideToggle(300);
            $(sessionObj).children('#expander').toggleClass('expanded');
        }

        function openSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideDown(300);
            $(sessionObj).children('#expander').addClass('expanded');
        }

        function closeSession(sessionObj) {
            $(sessionObj).children('[class$="-details"]').slideUp(300);
            $(sessionObj).children('#expander').removeClass('expanded');
        }

        function populateHiddenProgramTable() {

            /* if no posters were selected from either or both of the two poster sessions, we still want a row showing the main plenary poster session information for the unchosen session(s) */
            var posterSessionKeys = Object.keys(chosenPostersHash);
            if (posterSessionKeys.length == 0) {
                var sessionNames = ['session-poster-1', 'session-poster-2'];
                for (var i=0; i<sessionNames.length; i++) {
                    var session = sessionInfoHash[sessionNames[i]];
                    var exactSessionStartingTime = session.day + ', 2017 ' + session.start;
                    var newPlenaryKey = new Date(exactSessionStartingTime).getTime();
                    if (!(newPlenaryKey in plenarySessionHash)) {
                        plenarySessionHash[newPlenaryKey] = session;
                    }
                }
            }
            else if (posterSessionKeys.length == 1) {
                var posters = chosenPostersHash[posterSessionKeys[0]];
                var usedSession = posters[0].session;
                var unusedSession = usedSession == 'session-poster-1' ? sessionInfoHash['session-poster-2'] : sessionInfoHash['session-poster-1'];
                var exactSessionStartingTime = unusedSession.day + ', 2017 ' + unusedSession.start;
                var newPlenaryKey = new Date(exactSessionStartingTime).getTime();
                if (!(newPlenaryKey in plenarySessionHash)) {
                    plenarySessionHash[newPlenaryKey] = unusedSession;
                }
            }

            /* concatenate the tutorial, poster and paper keys */
            var nonPlenaryKeys = Object.keys(chosenPapersHash).concat(Object.keys(chosenTutorialsHash)).concat(Object.keys(chosenPostersHash));

            /* if we are including plenary information in the PDF then sort its keys too and merge the two sets of keys together before sorting */
            var sortedPaperTimes = includePlenaryInSchedule ? nonPlenaryKeys.concat(Object.keys(plenarySessionHash)) : nonPlenaryKeys;
            sortedPaperTimes.sort(function(a, b) { return a - b });

            /* now iterate over these sorted papers and create the rows for the hidden table that will be used to generate the PDF */
            var prevDay = null;
            var latestEndingTime;
            var output = [];

            /* now iterate over the chosen items */
            for(var i=0; i<sortedPaperTimes.length; i++) {
                var key = sortedPaperTimes[i];
                /* if it's a plenary session */
                if (key in plenarySessionHash) {
                    var plenarySession = plenarySessionHash[key];
                    if (plenarySession.day == prevDay) {
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    else {
                        output.push(makeDayHeaderRow(plenarySession.day));
                        output.push(makePlenarySessionHeaderRow(plenarySession));
                    }
                    prevDay = plenarySession.day;
                }
                /* if it's tutorials */
                else if (key in chosenTutorialsHash) {

                    /* get the tutorials */
                    var tutorials = chosenTutorialsHash[key];
                    var titles = tutorials.map(function(tutorial) { return ASCIIFold(tutorial.title); });
                    var locations = tutorials.map(function(tutorial) { return tutorial.location ; });
                    var sessions = tutorials.map(function(tutorial) { return sessionInfoHash[tutorial.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makeTutorialRows(tutorials[0].start, tutorials[0].end, titles, locations, sessions));
                    prevDay = sessionDay;
                }
                /* if it's posters */
                else if (key in chosenPostersHash) {

                    /* get the posters */
                    var posters = chosenPostersHash[key];

                    /* sort posters by their type for easier reading */
                    posters.sort(function(a, b) {
                        return a.type.localeCompare(b.type);
                    });
                    var titles = posters.map(function(poster) { return ASCIIFold(poster.title); });
                    var types = posters.map(function(poster) { return poster.type; });
                    var sessions = [sessionInfoHash[posters[0].session]];
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePosterRows(titles, types, sessions));
                    prevDay = sessionDay;
                }

                /* if it's papers  */
                else if (key in chosenPapersHash) {
                    var papers = chosenPapersHash[key];
                    /* sort papers by location for easier reading */
                    papers.sort(function(a, b) {
                        var aLocation = sessionInfoHash[a.session].location;
                        var bLocation = sessionInfoHash[b.session].location;
                        return aLocation.localeCompare(bLocation);
                    });
                    var titles = papers.map(function(paper) { return ASCIIFold(paper.title); });
                    var sessions = papers.map(function(paper) { return sessionInfoHash[paper.session]; });
                    var sessionDay = sessions[0].day;
                    if (sessionDay != prevDay) {
                        output.push(makeDayHeaderRow(sessionDay));
                    }
                    output = output.concat(makePaperRows(papers[0].start, papers[0].end, titles, sessions));
                    prevDay = sessionDay;
                }
            }

            /* append the output to the hidden table */
            $('#hidden-program-table tbody').append(output);
        }

        $(document).ready(function() {
            
            /* all the Remove All buttons are disabled on startup */
            $('.session-deselector').addClass('disabled');

            /* the include plenary checkbox is checked on startup */
            $('input#includePlenaryCheckBox').prop('checked', true);

            /* hide the testing notes */
            $('div#testingNotes').hide();

            /* show the floorplan when any location is clicked */
            $('span.session-location').magnificPopup({
                items: {
                    src: '/images/westin-floor-plan.png'
                },
                type: 'image'
            });
            
            /* get all the tutorial sessions and save the day and location for each of them in a hash */
            $('.session-tutorials').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the poster sessions and save the day and location for each of them in a hash */
            $('.session-posters').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+ [AP]M/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* get all the paper sessions and save the day and location for each of them in a hash */
            var paperSessions = $("[id|='session']").filter(function() { 
                return this.id.match(/session-\d[a-z]$/);
            });
            $(paperSessions).each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                var sessionTimeText = $(this).children('span.session-time').text().trim();                
                var sessionTimes = sessionTimeText.match(/\d+:\d+ [AP]M/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                sessionInfoHash[$(this).attr('id')] = session;
            });

            /* iterate over all the papers and store all their info in a hash since we need that info whenever we click and hover and lookups will be faster than re-computing the info at each event */
            $('tr#paper').each(function() {
                var paperID = $(this).attr('paper-id');

                /* get the paper session and day */
                var paperSession = $(this).parents('.session');
                var sessionDay = paperSession.prevAll('.day:first').text().trim();

                /* get the paper time and title */
                var paperTimeObj = $(this).children('#paper-time');
                var paperTitle = paperTimeObj.siblings('td').text().trim();

                /* get the paper slot and the starting and ending times */
                var paperTimeText = paperTimeObj.text().trim();
                var paperTimes = paperTimeText.split('-');
                var paperSlotStart = paperTimes[0];
                var paperSlotEnd = paperTimes[1];
                var paperSlotStartAMPM = inferAMPM(paperSlotStart);
                var paperSlotEndAMPM = inferAMPM(paperSlotEnd);
                var exactPaperStartingTime = sessionDay + ', 2017 ' + paperSlotStart + paperSlotStartAMPM;
                var exactPaperEndingTime = sessionDay + ', 2017 ' + paperSlotEnd + paperSlotEndAMPM;

                paperInfoHash[paperID] = [new Date(exactPaperStartingTime).getTime(), new Date(exactPaperEndingTime).getTime(), paperSlotStart, paperSlotEnd, paperTitle, paperSession.attr('id')];
            });

            /* also save the plenary session info in another hash since we may need to add this to the pdf. Use the exact starting time as the hash key */
             $('.session-plenary').each(function() {
                var session = {};
                session.title = $(this).children('.session-title').text().trim();
                session.location = $(this).children('span.session-location').text().trim();
                session.day = $(this).prevAll('.day:first').text().trim();
                session.id = $(this).attr('id');
                var sessionTimeText = $(this).children('span.session-time').text().trim();
                var sessionTimes = sessionTimeText.match(/\d+:\d+ [AP]M/g);
                var sessionStart = sessionTimes[0];
                var sessionEnd = sessionTimes[1];
                session.start = sessionStart;
                session.end = sessionEnd;
                var exactSessionStartingTime = session.day + ', 2017 ' + sessionStart;
                plenarySessionHash[new Date(exactSessionStartingTime).getTime()] = session;
             });

            $('body').on('click', 'a.session-selector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* if we are choosing the entire session, then basically "click" on all of the not-selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var unselectedPapers = sessionPapers.not('.selected');
                unselectedPapers.trigger('click', true);

                /* now find out how many papers are selected after the trigger */
                var selectedPapers = sessionPapers.filter('.selected');

                /* disable myself (the choose all button) */
                $(this).addClass('disabled');

                /* if we didn't have any papers selected earlier, then enable the remove all button */
                if (unselectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-deselector').removeClass('disabled');
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            $('body').on('click', 'a.session-deselector', function(event) {

                /* if we are disabled, do nothing */
                if ($(this).hasClass('disabled')) {
                    return false;
                }

                /* otherwise, if we are removing the entire session, then basically "click" on all of the already selected papers */
                var sessionPapers = $(this).siblings('table.paper-table').find('tr#paper');
                var selectedPapers = sessionPapers.filter('.selected');
                selectedPapers.trigger('click', true);

                /* disable myself (the remove all button) */
                $(this).addClass('disabled');

                /* enable the choose all button */
                $(this).siblings('session-deselector').removeClass('disabled');

                /* if all the papers were selected earlier, then enable the choose all button */
                if (selectedPapers.length == sessionPapers.length) {
                    $(this).siblings('.session-selector').removeClass('disabled');                    
                }

                /* this is not really a link */
                event.preventDefault();
                return false;
            });

            /* hide all of the session details when starting up */
            $('[class$="-details"]').hide();

            /* expand sessions when their title is clicked */
            $('body').on('click', 'div.session-expandable .session-title', function(event) {
                event.preventDefault();
                event.stopPropagation();
                var sessionObj = $(this).parent();

                /* if we had the shift key pressed, then expand ALL unexpanded parallel sessions including myself (only for papers) */
                if (event.shiftKey && sessionObj.attr('class').match('session-papers')) {
                    var sessionId = $(sessionObj).attr('id').match(/session-\d/)[0];
                    var parallelSessions = $(sessionObj).siblings().addBack().filter(function() { return this.id.match(sessionId); });

                    var unexpandedParallelSessions = $(parallelSessions).filter(function() { return !$(this).children('#expander').hasClass('expanded'); })

                    /* if all sessions are already expanded, then shift-clicking should close all of them */
                    if (unexpandedParallelSessions.length == 0) {
                        $.map(parallelSessions, closeSession);
                    }
                    else {
                        $.map(unexpandedParallelSessions, openSession);
                    }
                } 
                /* for a regular click, just toggle the individual session */
                else {
                    toggleSession(sessionObj);
                }
            });

            /* when we mouse over a paper, highlight the conflicting papers */
            $('body').on('mouseover', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).addClass('hovered');
                $(conflictingPapers).addClass('conflicted');
            });

            /* when we mouse out, remove all highlights */
            $('body').on('mouseout', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).removeClass('hovered');
                $(conflictingPapers).removeClass('conflicted');

            });

            $('body').on('click', 'a.inline-location', function(event) {
                return false;
            });

            $('body').on('click', 'span.session-location', function(event) {
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

            $('body').on('click', 'table.tutorial-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'table.poster-table', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'div.paper-session-details', function(event) {
                event.stopPropagation();
            });

            $('body').on('click', 'input#includePlenaryCheckBox', function(event) {
                    includePlenaryInSchedule = $(this).prop('checked');
            });

            $('body').on('click', 'a#generatePDFButton', function(event) {
                /* if we haven't chosen any papers, and we aren't including plenary sessions either, then raise an error. If we are including plenary sessions and no papers, then confirm. */
                event.preventDefault();
                var numChosenItems = Object.keys(chosenPapersHash).length + Object.keys(chosenTutorialsHash).length + Object.keys(chosenPostersHash).length;
                if (numChosenItems == 0) {
                    if (includePlenaryInSchedule) {
                        vex.dialog.confirm({
                            message: "The PDF will contain only the plenary sessions since nothing was chosen. Proceed?",
                            callback: function (value) {
                                if (value) {
                                    generatePDFfromTable();
                                }
                                else {
                                    return false;
                                }
                            }
                        });
                    }
                    else {
                        vex.dialog.alert('Nothing to generate. Nothing was chosen and plenary sessions were excluded.');
                        return false;
                    }
                }
                else {
                    generatePDFfromTable();
                }
            });

            $('body').on('click', 'table.tutorial-table tr#tutorial', function(event) {
                event.preventDefault();
                var tutorialTimeObj = $(this).parents('.session-tutorials').children('.session-time');
                var tutorialInfo = getTutorialInfoFromTime(tutorialTimeObj);
                var tutorialObject = {};
                var exactStartingTime = tutorialInfo[0];
                tutorialObject.start = tutorialInfo[1];
                tutorialObject.end = tutorialInfo[2];
                tutorialObject.title = $(this).find('.tutorial-title').text();
                tutorialObject.session = tutorialInfo[3];
                tutorialObject.location = $(this).find('.inline-location').text();
                tutorialObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected tutorial */
                if (isChosen(exactStartingTime, tutorialObject, 'tutorial')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, tutorialObject, 'tutorial');
                }
                else {
                    addToChosen(exactStartingTime, tutorialObject, 'tutorial');
                    $(this).addClass('selected');                    
                }
            });

            $('body').on('click', 'table.poster-table tr#poster', function(event) {
                event.preventDefault();
                var posterTimeObj = $(this).parents('.session-posters').children('.session-time');
                var posterInfo = getPosterInfoFromTime(posterTimeObj);
                var posterObject = {};
                var exactStartingTime = posterInfo[0];
                posterObject.start = posterInfo[1];
                posterObject.end = posterInfo[2];
                posterObject.title = $(this).find('.poster-title').text().trim();
                posterObject.type = $(this).parents('.poster-table').prevAll('.poster-type:first').text().trim();
                posterObject.session = posterInfo[3];
                posterObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected poster */
                if (isChosen(exactStartingTime, posterObject, 'poster')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, posterObject, 'poster');
                }
                else {
                    addToChosen(exactStartingTime, posterObject, 'poster');
                    $(this).addClass('selected');
                    var key = new Date(exactStartingTime).getTime();
                    if (key in plenarySessionHash) {
                        delete plenarySessionHash[key];
                    }
                }
            });

            $('body').on('click', 'table.paper-table tr#paper', function(event, fromSession) {
                event.preventDefault();
                $(this).removeClass('hovered');
                getConflicts($(this)).removeClass('conflicted');
                var paperID = $(this).attr('paper-id');
                var paperTimeObj = $(this).children('td#paper-time');
                var paperInfo = paperInfoHash[paperID];
                var paperObject = {};
                var exactStartingTime = paperInfo[0];
                paperObject.start = paperInfo[2];
                paperObject.end = paperInfo[3];
                paperObject.title = paperInfo[4];
                paperObject.session = paperInfo[5];
                paperObject.exactStartingTime = exactStartingTime;

                /* if we are clicking on an already selected paper */
                if (isChosen(exactStartingTime, paperObject, 'paper')) {
                    $(this).removeClass('selected');
                    removeFromChosen(exactStartingTime, paperObject, 'paper');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {
        
                        /* we also need to enable the choose button */
                        $(this).parents('table.paper-table').siblings('.session-selector').removeClass('disabled');

                        /* we also need to disable the remove button if this was the only paper selected in the session */
                        var selectedPapers = $(this).siblings('tr#paper').filter('.selected');
                        if (selectedPapers.length == 0) {
                            $(this).parents('table.paper-table').siblings('.session-deselector').addClass('disabled');
                        }
                    }
                }
                else {
                    /* if we are selecting a previously unselected paper */
                    addToChosen(exactStartingTime, paperObject, 'paper');
                    $(this).addClass('selected');

                    /* if we are not being triggered at the session level, then we need to handle the state of the session level button ourselves */
                    if (!fromSession) {

                        /* we also need to enable the remove button */
                        $(this).parents('table.paper-table').siblings('.session-deselector').removeClass('disabled');

                        /* and disable the choose button if all the papers are now selected anyway */
                        var sessionPapers = $(this).siblings('tr#paper');
                        var selectedPapers = sessionPapers.filter('.selected');
                        if (sessionPapers.length == selectedPapers.length) {
                            $(this).parents('table.paper-table').siblings('.session-selector').addClass('disabled');
                        }
                    }
                }
            });
        });
    </script>
---
{% include base_path %}

<link rel="stylesheet" href="/assets/css/vex.css" />
<link rel="stylesheet" href="/assets/css/vex-theme-wireframe.css" />

<table id="hidden-program-table">
    <thead>
        <tr><th>time</th><th>location</th><th>info</th></tr>
    </thead>
    <tbody></tbody>
</table>

<div id="testingInstructions" style="font-size: smaller;">
    <p>Welcome, testers! Thank you for helping us test the ACL 2017 conference program page. </p>
    
    <p>For the first time, the program page will allow conference attendees to choose the sessions (or individual paper talks) they want to attend <em>and</em> generate a PDF of their customized schedule! </p>

    <strong>Instructions &amp; Notes</strong>:
    <ul>
        <li>Click on the title of a session to expand and collapse the session. On a non-mobile browser, you can also click anywhere in the cell containing the session title.</li>
        <li>Click on a tutorial/paper/poster to select it, click again to unselect it.</li>
        <li>You can select more than one paper for a time slot.</li>
        <li>When you hover on a paper for a time slot, it is highlighted in yellow along with the conflicting papers to make the comparison easier. This only works on non-mobile devices where parallel sessions are displayed adjacent to each other.</li>
        <li>If papers are already selected for a time slot, hovering highlights them in green.</li>
        <li>Click on the <em>Generate PDF</em> button at the bottom of the page to generate the PDF for your selected talks.</li>
        <li>Since ACL 2017 doesn't have a program yet, we used the content from the NAACL 2016 conference for the purposes of testing.</li>
        <li>The page has been tested on MacOS 10.12.3 on the most recent versions of Chrome, Firefox, and Safari browsers. We would like to test on other OSes (Windows, Linux) and other browsers, although older browsers (e.g., Internet Explorer <= v10) will likely not work. </li>
        <li>The page has also been tested on an iPhone simulator and works as expected. However, it'd be nice to test it on Android (<strong>NOTE</strong>: only Chrome on Android will work).</li>
        <li>Note that if you are using Safari, you will need to use <em>Cmd-P</em> to print and <em>File > Save as ... </em>to download the schedule. Chrome and Firefox have buttons for printing and saving as part of their PDF rendering UI.</li>
        <li>The generated PDF might have some blank rows at the bottom as padding since the PDF generation has been programmed to avoid rows being split across pages.</li>
        <li>While saving the generated PDF on mobile devices, its name cannot be changed.</li>
        <li><strong>Please report any issues or problems you run into <a href="https://github.com/acl2017/acl2017.github.io/issues/new" target="_blank">here</a>. You will need a GitHub account.</strong></li>
    </ul>
</div>

<div class="schedule">
    <div class="day" id="first-day">Sunday, July 30</div>
    <div class="session session-expandable session-tutorials" id="session-morning-tutorials">
        <div id="expander"></div><a href="#" class="session-title">Morning Tutorials</a><br/>
        <span class="session-time">9:30 AM &ndash; 12:30 PM</span><br/>
        <div class="tutorial-session-details">
            <hr class="detail-separator"/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T1] Natural Language Processing for Precision Medicine </span><br/><span class="btn btn--location inline-location">Mackenzie</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T2] Multimodal Machine Learning </span><br/><span href="#" class="btn btn--location inline-location">Salon 1</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T3] Deep Learning for Semantic Composition </span><br/><span href="#" class="btn btn--location inline-location">Salons B/C</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-lunch-1">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 2:00 PM</span>
    </div>
    <div class="session session-expandable session-tutorials" id="session-afternoon-tutorials">
        <div id="expander"></div><a href="#" class="session-title">Afternoon Tutorials</a><br/>
        <span class="session-time">2:00 PM &ndash; 5:30 PM</span><br/>
        <div class="tutorial-session-details">
            <hr class="detail-separator"/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T4] Deep Learning for Dialogue Systems </span><br/><span class="btn btn--location inline-location">Salons B/C</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T5] Beyond Words: Deep Learning for Multi-word Expressions and Collocations </span><br/><span href="#" class="btn btn--location inline-location">Salon 1</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T6] Making Better Use of the Crowd</span><br/><span href="#" class="btn btn--location inline-location">Mackenzie</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-reception">
        <div id="expander"></div><a href="#" class="session-title">Welcome Reception</a><br/>        
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grand Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Catch up with your colleagues at the Welcome Reception!  It will be held immediately following the tutorials at the Westin Bayshore Hotel, Sunday, July 30th, in the Bayshore Grand Ballroom (the conference venue).  Refreshments and a light dinner will be provided and a cash bar will be available.</p>
            </div>
        </div>
    </div>
<div class="day" id="second-day">Monday, July 31</div>
    <div class="session session-plenary" id="session-breakfast-1">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-plenary" id="session-welcome">
        <span class="session-title">Welcome Session / Presidential Address</span><br/>        
        <span class="session-people">Chris Callison-Burch, Regina Barzilay, Min-Yen Kan, and Marti Hearst</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:00 AM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grande Ballroom</span>
    </div>
    <div class="session session-plenary" id="session-break-1">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:00 AM &ndash; 10:30 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-1a">
        <div id="expander"></div><a href="#" class="session-title">Information Extraction 1</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="1">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Adversarial Multi-task Learning for Text Classification. </span><em>Pengfei Liu, Xipeng Qiu and Xuanjing Huang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="2">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Neural End-to-End Learning for Computational Argumentation Mining. </span><em>Steffen Eger, Johannes Daxenberger and Iryna Gurevych</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="3">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Neural Symbolic Machines: Learning Semantic Parsers on Freebase with Weak Supervision. </span><em>Chen Liang, Jonathan Berant, Quoc Le, Kenneth D. Forbus and Ni Lao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="4">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Neural Relation Extraction with Multi-lingual Attention. </span><em>Yankai Lin, Zhiyuan Liu and Maosong Sun</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="5">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">Classifying Temporal Relations by Bidirectional LSTM over Dependency Paths. </span><em>Fei Cheng and Yusuke Miyao</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-1b">
        <div id="expander"></div><a href="#" class="session-title">Semantics 1</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="6">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Inducing Symbolic Meaning Representations for Semantic Parsing. </span><em>Jianpeng Cheng, Siva Reddy, Vijay Saraswat and Mirella Lapata</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="7">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Morph-fitting: Fine-Tuning Word Vector Spaces with Simple Language-Specific Rules. </span><em>Ivan Vulić, Nikola Mrkšić, Roi Reichart, Diarmuid Ó Séaghdha, Steve Young and Anna Korhonen</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="8">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Skip-Gram – Zipf + Uniform = Vector Additivity. </span><em>Alex Gittens, Dimitris Achlioptas and Michael W. Mahoney</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="9">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">The State of the Art in Semantic Representation. </span><em>Omri Abend and Ari Rappoport</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="10">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">AMR-to-text Generation with Synchronous Node Replacement Grammar. </span><em>Linfeng Song, Xiaochang Peng, Yue Zhang, Zhiguo Wang and Daniel Gildea</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-1c">
        <div id="expander"></div><a href="#" class="session-title">Discourse 1</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="11">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Joint Learning for Coreference Resolution. </span><em>Jing Lu and Vincent Ng</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="12">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Generating and Exploiting Large-scale Pseudo Training Data for Zero Pronoun Resolution. </span><em>Ting Liu, Yiming Cui, Qingyu Yin, Wei-Nan Zhang, Shijin Wang and Guoping Hu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="13">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Discourse Mode Identification in Essays. </span><em>Wei Song</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="14">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Winning on the Merits: The Joint Effects of Content and Style on Debate Outcomes. </span><em>Lu Wang, Nick Beauchamp, Sarah Shugars, Kechen Qin</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="15">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">Lexical Features in Coreference Resolution: To be Used With Caution. </span><em>Nafise Sadat Moosavi and Michael Strube</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-1d">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation 1</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="16">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">A Convolutional Encoder Model for Neural Machine Translation. </span><em>Jonas Gehring, Michael Auli, David Grangier and Yann Dauphin</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="17">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Deep Neural Machine Translation with Linear Associative Unit. </span><em>Mingxuan Wang, Zhengdong Lu, Jie Zhou and Qun Liu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="18">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">A Polynomial-Time Dynamic Programming Algorithm for Phrase-Based Decoding with a Fixed Distortion Limit. </span><em>Yin-Wen Chang and Michael Collins</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="19">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Context Gates for Neural Machine Translation. </span><em>Zhaopeng Tu, Yang Liu, Zhengdong Lu, Xiaohua Liu, and Hang Li</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="20">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">Alternative Objective Functions for Training MT Evaluation Metrics. </span><em>Miloš Stanojević and Khalil Sima’an</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-1e">
        <div id="expander"></div><a href="#" class="session-title">Generation</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="21">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Neural AMR: Sequence-to-Sequence Models for Parsing and Generation. </span><em>Ioannis Konstas, Srinivasan Iyer, Mark Yatskar, Yejin Choi and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="22">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Program Induction for Rationale Generation: Learning to Solve and Explain Algebraic Word Problems. </span><em>Wang Ling, Dani Yogatama, Chris Dyer and Phil Blunsom</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="23">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Automatically Generating Rhythmic Verse with Neural Networks. </span><em>Jack Hopkins and Douwe Kiela</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="24">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Creating Training Corpora for Micro-Planners. </span><em>Claire Gardent, Anastasia Shimorina, Shashi Narayan and Laura Perez-Beltrachini</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="25">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">A Principled Framework for Evaluating Summarizers: Comparing Models of Summary Quality against Human Judgments. </span><em>Maxime Peyrard and Judith Eckle-Kohler</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>        
    <div class="session session-plenary" id="session-lunch-2">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:00 PM &ndash; 1:40 PM</span>
    </div>    
    <div class="session session-expandable session-papers1" id="session-2a">
        <div id="expander"></div><a href="#" class="session-title">Question Answering</a><br/>
            <span class="session-time">1:40 PM &ndash; 3:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="26">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Gated Self-Matching Networks for Reading Comprehension and Question Answering. </span><em>Wenhui Wang, Nan Yang, Furu Wei, Baobao Chang and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="27">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Generating Natural Answer by Incorporating Copying and Retrieving Mechanisms in Sequence-to-Sequence Learning. </span><em>Shizhu He, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="28">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Coarse-to-Fine Question Answering for Long Documents. </span><em>Eunsol Choi, Daniel Hewlett, Illia Polosukhin, Alexandre Lacoste, Jakob Uszkoreit and Jonathan Berant</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="29">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">An End-to-End Model for Question Answering over Knowledge Base with Cross-Attention Combining Global Knowledge. </span><em>Yanchao Hao, Yuanzhe Zhang, Shizhu He, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="30">
                        <td id="paper-time">2:56-3:14</td>
                        <td>
                            <span class="paper-title">Domain-Targeted, High Precision Knowledge Extraction. </span><em>Bhavana Dalvi, Niket Tandon, Peter Clark</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-2b">
        <div id="expander"></div><a href="#" class="session-title">Vision 1</a><br/>
            <span class="session-time">1:40 PM &ndash; 3:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="31">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Translating Neuralese. </span><em>Jacob Andreas, Anca Dragan and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="32">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Combining distributional and referential information for naming objects through cross-modal mapping and direct word prediction. </span><em>Sina Zarrieß and David Schlangen</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="33">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">FOIL it! Find One mismatch between Image and Language caption. </span><em>Ravi Shekhar, Sandro Pezzelle, Yauhen Klimovich, Aurélie Herbelot, Moin Nabi, Enver Sangineto and Raffaella Bernardi</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="34">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Verb Physics: Relative Physical Knowledge of Actions and Objects. </span><em>Maxwell Forbes and Yejin Choi</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="35">
                        <td id="paper-time">2:56-3:14</td>
                        <td>
                            <span class="paper-title">Visually Grounded and Textual Semantic Models Differentially Decode Brain Activity Associated with Concrete and Abstract Nouns. </span><em>Andrew J. Anderson, Douwe Kiela, Stephen Clark, Massimo Poesio</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-2c">
        <div id="expander"></div><a href="#" class="session-title">Syntax 1</a><br/>
            <span class="session-time">1:40 PM &ndash; 3:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="36">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">A* CCG Parsing with a Supertag and Dependency Factored Model. </span><em>Masashi Yoshikawa, Hiroshi Noji and Yuji Matsumoto</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="37">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">A Full Non-Monotonic Transition System for Unrestricted Non-Projective Parsing. </span><em>Daniel Fernández-González and Carlos Gómez-Rodríguez</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="38">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Aggregating and Predicting Sequence Labels from Crowd Annotations. </span><em>An Thanh Nguyen, Byron Wallace, Junyi Jessy Li, Ani Nenkova and Matthew Lease</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="39">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Fine-Grained Prediction of Syntactic Typology: Discovering Latent Structure with Supervised Learning. </span><em>Dingquan Wang and Jason Eisner</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="40">
                        <td id="paper-time">2:56-3:14</td>
                        <td>
                            <span class="paper-title">Learning to Prune: Exploring the Frontier of Fast and Accurate Parsing. </span><em>Tim Vieira, Jason Eisner</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-2d">
        <div id="expander"></div><a href="#" class="session-title">Machine Learning 1</a><br/>
            <span class="session-time">1:40 PM &ndash; 3:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="41">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Multi-space Variational Encoder-Decoders for Semi-supervised Labeled Sequence Transduction. </span><em>Chunting Zhou and Graham Neubig</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="42">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Scalable Bayesian Learning of Recurrent Neural Networks for Language Modeling. </span><em>Zhe Gan, Chunyuan Li, Changyou Chen, Yunchen Pu, Qinliang Su and Lawrence Carin</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="43">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Learning attention for historical text normalization by learning to pronounce. </span><em>Marcel Bollmann, Joachim Bingel and Anders Søgaard</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="44">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Deep Learning in Semantic Kernel Spaces. </span><em>Danilo Croce, Simone Filice, Giuseppe Castellucci and Roberto Basili</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="45">
                        <td id="paper-time">2:56-3:14</td>
                        <td>
                            <span class="paper-title">Topically Driven Neural Language Model. </span><em>Jey Han Lau, Timothy Baldwin and Trevor Cohn</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>    
    <div class="session session-expandable session-papers5" id="session-2e">
        <div id="expander"></div><a href="#" class="session-title">Sentiment 1</a><br/>
            <span class="session-time">1:40 PM &ndash; 3:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="46">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Handling Cold-Start Problem in Review Spam Detection by Jointly Embedding Texts and Behaviors. </span><em>Xuepeng Wang, Jun Zhao and Kang Liu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="47">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Learning Cognitive Features from Gaze Data for Sentiment and Sarcasm Classification using Convolutional Neural Network. </span><em>Abhijit Mishra, Kuntal Dey and Pushpak Bhattacharyya</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="48">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">An Unsupervised Neural Attention Model for Aspect Extraction. </span><em>Ruidan He, Wee Sun Lee, Hwee Tou Ng and Daniel Dahlmeier</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="49">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Other Topics You May Also Agree or Disagree: Modeling Inter-Topic Preferences using Tweets and Matrix Factorization. </span><em>Akira Sasaki, Kazuaki Hanawa, Naoaki Okazaki and Kentaro Inui</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="50">
                        <td id="paper-time">2:56-3:14</td>
                        <td>
                            <span class="paper-title">Overcoming Language Variation in Sentiment Analysis with Social Attention. </span><em>Yi Yang, Jacob Eisenstein</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-plenary" id="session-break-2">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:15 PM &ndash; 3:45 PM</span>
    </div>   
    <div class="session session-expandable session-papers1" id="session-3a">
        <div id="expander"></div><a href="#" class="session-title">Information Extraction 2</a><br/>
            <span class="session-time">3:45 PM &ndash; 5:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="51">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Automatically Labeled Data Generation for Large Scale Event Extraction. </span><em>Yubo Chen, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="52">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Time Expression Analysis and Recognition Using Syntactic Token Types and General Heuristic Rules. </span><em>Xiaoshi Zhong, Aixin Sun and Erik Cambria</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="53">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Learning with Noise: Enhance Distantly Supervised Relation Extraction with Dynamic Transition Matrix. </span><em>Bingfeng Luo, Yansong Feng, Zheng Wang, Zhanxing Zhu, Songfang Huang, Rui Yan and Dongyan Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="54">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Ordinal Common-sense Inference. </span><em>Sheng Zhang, Rachel Rudinger, Kevin Duh, Benjamin Van Durme</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="55">
                        <td id="paper-time">5:01-5:13</td>
                        <td>
                            <span class="paper-title">Vector space models for evaluating semantic fluency in autism. </span><em>Emily Prud’hommeaux, Jan van Santen and Douglas Gliner</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-3b">
        <div id="expander"></div><a href="#" class="session-title">Semantics 2</a><br/>
            <span class="session-time">3:45 PM &ndash; 5:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="56">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">A Syntactic Neural Model for General-Purpose Code Generation. </span><em>Pengcheng Yin and Graham Neubig</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="57">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Learning bilingual word embeddings with (almost) no bilingual data. </span><em>Mikel Artetxe, Gorka Labaka and Eneko Agirre</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="58">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Abstract Meaning Representation Parsing using LSTM Recurrent Neural Networks. </span><em>William Foland and James H. Martin</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="59">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Deep Semantic Role Labeling: What Works and What’s Next. </span><em>Luheng He, Kenton Lee, Mike Lewis and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="60">
                        <td id="paper-time">5:01-5:13</td>
                        <td>
                            <span class="paper-title">Neural Architectures for Multilingual Semantic Parsing. </span><em>Raymond Hendy Susanto and Wei Lu</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-3c">
        <div id="expander"></div><a href="#" class="session-title">Speech / Dialogue 1</a><br/>
            <span class="session-time">3:45 PM &ndash; 5:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="61">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Towards End-to-End Reinforcement Learning of Dialogue Agents for Information Access. </span><em>Bhuwan Dhingra, Lihong Li, Xiujun Li, Jianfeng Gao, Yun-Nung Chen, Faisal Ahmed and Li Deng</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="62">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Sequential Matching Network: A New Architecture for Multi-turn Response Selection in Retrieval-based Chatbots. </span><em>Yu Wu, Wei Wu, Chen Xing, Ming Zhou and Zhoujun Li</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="63">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Learning Word-Like Units from Joint Audio-Visual Analysis. </span><em>David Harwath and James Glass</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="64">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Joint CTC-attention End-to-end Speech Recognition. </span><em>Shinji Watanabe, Takaaki Hori and John Hershey</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="65">
                        <td id="paper-time">5:01-5:13</td>
                        <td>
                            <span class="paper-title">Incorporating Uncertainty into Deep Learning for Spoken Language Assessment. </span><em>Andrey Malinin, Anton Ragni, Kate Knill and Mark Gales</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-3d">
        <div id="expander"></div><a href="#" class="session-title">Multilingual</a><br/>
            <span class="session-time">3:45 PM &ndash; 5:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="66">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Found in Translation: Reconstructing Phylogenetic Language Trees from Translations. </span><em>Ella Rabinovich, Noam Ordan and Shuly Wintner</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="67">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Predicting Native Language from Gaze. </span><em>Yevgeni Berzak, Chie Nakamura, Suzanne Flynn and Boris Katz</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="68">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Decoding Anagrammed Texts Written in an Unknown Language and Script. </span><em>Bradley Hauer and Grzegorz Kondrak</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="69">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Sparse Coding of Neural Word Embeddings for Multilingual Sequence Labeling. </span><em>Gábor Berend</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="70">
                        <td id="paper-time">5:01-5:13</td>
                        <td>
                            <span class="paper-title">Incorporating Dialectal Variability for Socially Equitable Language Identification. </span><em>David Jurgens, Yulia Tsvetkov and Dan Jurafsky</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-3e">
        <div id="expander"></div><a href="#" class="session-title">Phonology</a><br/>
            <span class="session-time">3:45 PM &ndash; 5:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="71">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">MORSE: Semantic-ally Drive-n MORpheme SEgment-er. </span><em>Tarek Sakakini, Suma Bhat and Pramod Viswanath</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="72">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">A Generative Model of Phonotactics. </span><em>Richard Futrell, Adam Albright, Peter Graff, and Timothy J. O’Donnell</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="73">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Joint Semantic Synthesis and Morphological Analysis of the Derived Word. </span><em>Ryan Cotterell and Hinrich Schütze</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="74">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Unsupervised Learning of Morphological Forests. </span><em>Jiaming Luo, Karthik, Narasimhan</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="75">
                        <td id="paper-time">5:01-5:13</td>
                        <td>
                            <span class="paper-title">Evaluation of Compound Splitting with Textual Entailment. </span><em>Glorianna Jagfeld, Patrick Ziering and Lonneke van der Plas</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>        
    <div class="session session-expandable session-posters" id="session-poster-1">
        <div id="expander"></div><a href="#" class="session-title">Posters &amp; Dinner</a><br/>        
        <span class="session-time">6:20 PM &ndash; 9:50 PM</span>
        <br/>
        <span class="session-location btn btn--location">Bayshore Grand Foyer/Stanley Park Foyer/Cypress</span>
        <div class="poster-session-details">
            <hr class="detail-separator"/>
            <h4 class="poster-type" style="text-decoration: underline;">Long Papers</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Enriching Complex Networks with Word Embeddings for Detecting Mild Cognitive Impairment from Speech Transcripts. </span><em>Leandro Santos, Edilson Anselmo Corrêa Júnior, Osvaldo Oliveira Jr, Diego Amancio, Letícia Mansur and Sandra Aluísio</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Adversarial Adaptation of Synthetic or Stale Data. </span><em>Young-Bum Kim, Karl Stratos and Dongchan Kim</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Chat Detection in Intelligent Assistant: Combining Task-oriented and Non-task-oriented Spoken Dialogue Systems. </span><em>Satoshi Akasaki and Nobuhiro Kaji</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Neural Local Coherence Model. </span><em>Shafiq Joty and Dat Tien Nguyen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Data-Driven Broad-Coverage Grammars for Opinionated Natural Language Generation (ONLG). </span><em>Tomer Cagan, Stefan L. Frank and Reut Tsarfaty</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Ask: Neural Question Generation for Reading Comprehension. </span><em>Xinya Du, Junru Shao and Claire Cardie</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Joint Optimization of User-desired Content in Multi-document Summaries by Learning from User Feedback. </span><em>Avinesh PVS and Christian M. Meyer</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Flexible and Creative Chinese Poetry Generation Using Neural Memory. </span><em>Jiyuan Zhang, Yang Feng, Dong Wang, Yang Wang, Andrew Abel, Shiyue Zhang and Andi Zhang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Generate Market Comments from Stock Prices. </span><em>Soichiro Murakami, Akihiko Watanabe, Akira Miyazawa, Keiichi Goshima, Toshihiko Yanase, Hiroya Takamura and Yusuke Miyao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Can Syntax Help? Improving an LSTM-based Sentence Compression Model for New Domains. </span><em>Liangguo Wang, Jing Jiang, Hai Leong Chieu, Hui Ong Ong, Dandan Song and Lejian Liao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Transductive Non-linear Learning for Chinese Hypernym Prediction. </span><em>Chengyu Wang, Xiaofeng He and Aoying Zhou</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Constituent-Centric Neural Architecture for Reading Comprehension. </span><em>Pengtao Xie and Eric Xing</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-lingual Distillation for Text Classification. </span><em>Ruochen Xu and Yiming Yang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Understanding and Predicting Empathic Behavior in Counseling Therapy. </span><em>Verónica Pérez-Rosas, Rada Mihalcea, Kenneth Resnicow, Satinder Singh and Lawrence An</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Leveraging Knowledge Bases in LSTMs for Improving Machine Reading. </span><em>Bishan Yang and Tom Mitchell</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Prerequisite Relation Learning for Concepts in MOOCs. </span><em>Liangming Pan, Chengjiang Li, Juanzi Li and Jie Tang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Unsupervised Text Segmentation Based on Native Language Characteristics. </span><em>Shervin Malmasi, Mark Dras, Mark Johnson, Lan Du and Magdalena Wolska</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Weakly Supervised Cross-Lingual Named Entity Recognition via Effective Annotation and Representation Projection. </span><em>Jian Ni, Georgiana Dinu and Radu Florian</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Context Sensitive Lemmatization Using Two Successive Bidirectional Gated Recurrent Networks. </span><em>Abhisek Chakrabarty, Onkar Arun Pandit and Utpal Garain</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Create and Reuse Words in Open-Vocabulary Neural Language Modeling. </span><em>Kazuya Kawakami, Chris Dyer and Phil Blunsom</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bandit Structured Prediction for Neural Sequence-to-Sequence Learning. </span><em>Julia Kreutzer, Artem Sokolov and Stefan Riezler</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Prior Knowledge Integration for Neural Machine Translation using Posterior Regularization. </span><em>Jiacheng Zhang, Yang Liu, Huanbo Luan, Jingfang Xu and Maosong Sun</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Incorporating Word Reordering Knowledge into Attention-based Neural Machine Translation. </span><em>Jinchao Zhang, Mingxuan Wang, Qun Liu and Jie Zhou</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Lexically Constrained Decoding for Sequence Generation Using Grid Beam Search. </span><em>Chris Hokamp and Qun Liu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Combating Human Trafficking with Multimodal Deep Models. </span><em>Edmund Tong, Amir Zadeh and Louis-Philippe Morency</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">MalwareTextDB: A Database for Annotated Malware Articles. </span><em>Swee Kiat Lim, Aldrian Obaja Muis, Wei Lu and Chen Hui Ong</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Corpus of Annotated Revisions for Studying Argumentative Writing. </span><em>Fan Zhang, Homa B. Hashemi, Rebecca Hwa and Diane Litman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatic Induction of Synsets from a Graph of Synonyms. </span><em>Dmitry Ustalov, Alexander Panchenko and Chris Biemann</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Neural Modeling of Multi-Predicate Interactions for Japanese Predicate Argument Structure Analysis. </span><em>Hiroki Ouchi, Hiroyuki Shindo and Yuji Matsumoto</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension. </span><em>Mandar Joshi, Eunsol Choi, Daniel Weld and Luke Zettlemoyer</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Translational Semantic Correspondences in Technical Documentation. </span><em>Kyle Richardson and Jonas Kuhn</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bridge Text and Knowledge by Learning Multi-Prototype Entity Mention Embedding. </span><em>Yixin Cao, Lifu Huang, Heng Ji, Xu Chen and Juanzi Li</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Interactive Learning for Acquisition of Grounded Verb Semantics towards Human-Robot Communication. </span><em>Lanbo She and Joyce Chai</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Multimodal Word Distributions. </span><em>Ben Athiwaratkun and Andrew Wilson</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Enhanced LSTM for Natural Language Inference. </span><em>Qian Chen, Xiaodan Zhu, Zhen-Hua Ling, Si Wei, Hui Jiang and Diana Inkpen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Linguistic analysis of differences in portrayal of movie characters. </span><em>Anil Ramakrishna, Victor R. Martínez, Nikolaos Malandrakis, Karan Singla and Shrikanth Narayanan</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Linguistically Regularized LSTM for Sentiment Classification. </span><em>Qiao Qian, Minlie Huang and Xiaoyan Zhu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sarcasm SIGN: Interpreting Sarcasm with Sentiment Based Monolingual Machine Translation. </span><em>Lotem Peled and Roi Reichart</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Active Sentiment Domain Adaptation. </span><em>Fangzhao Wu and Yongfeng Huang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Volatility Prediction using Financial Disclosures Sentiments with Word Embedding-based IR Models. </span><em>Navid Rekabsaz, Mihai Lupu, Artem Baklanov, Alexander Dür, Linda Andersson and Allan Hanbury</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">CANE: Context-Aware Network Embedding for Relation Modeling. </span><em>Cunchao Tu, Han Liu, Zhiyuan Liu and Maosong Sun</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Universal Dependencies Parsing for Colloquial Singaporean English. </span><em>Hongmin Wang, Yue Zhang, GuangYong Leonard Chan, Jie Yang and Hai Leong Chieu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Generic Axiomatization of Families of Noncrossing Graphs in Dependency Parsing. </span><em>Anssi Yli-Jyrä and Carlos Gómez-Rodríguez</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Semi-supervised sequence tagging with bidirectional language models. </span><em>Matthew Peters, Waleed Ammar, Chandra Bhagavatula and Russell Power</em>
                    </td>
                </tr>
            </table>
            <h4 class="poster-type" style="text-decoration: underline;">Short Papers</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Neural Architecture for Temporal Relation Extraction: A Bi-LSTM Approach for Detecting Narrative Containers. </span><em>Julien Tourille, Olivier Ferret, Aurelie Neveol and Xavier Tannier</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">How to Make Contexts More Useful? An Empirical Study to Context-Aware Neural Conversation Models. </span><em>Zhiliang Tian, Rui Yan, Lili Mou, Yiping Song, Yansong Feng and Dongyan Zhao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-lingual and cross-domain discourse segmentation of entire documents. </span><em>Chloé Braud, Ophélie Lacroix and Anders Søgaard</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Detecting Good Arguments in a Non-Topic-Specific Way: An Oxymoron?. </span><em>Beata Beigman Klebanov, Binod Gyawali and Yi Song</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Argumentation Quality Assessment: Theory vs. Practice. </span><em>Henning Wachsmuth, Nona Naderi, Ivan Habernal, Yufang Hou, Graeme Hirst, Iryna Gurevych and Benno Stein</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Recurrent Neural Model with Attention for the Recognition of Chinese Implicit Discourse Relations. </span><em>Niko Schenk and Samuel Rönnqvist</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Discourse Annotation of Non-native Spontaneous Spoken Responses Using the Rhetorical Structure Theory Framework. </span><em>Xinhao Wang, James Bruno, Hillary Molloy, Keelan Evanini and Klaus Zechner</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving Implicit Discourse Relation Recognition with Discourse-specific Word Embeddings. </span><em>Changxing Wu, Xiaodong Shi, Yidong Chen, Jinsong Su and Boli Wang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Oracle Summaries of Compressive Summarization. </span><em>Tsutomu Hirao, Masaaki Nishino and Masaaki Nagata</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Japanese Sentence Compression with a Large Training Dataset. </span><em>Shun Hasegawa, Yuta Kikuchi, Hiroya Takamura and Manabu Okumura</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Generate Natural Language Descriptions From Source Code Changes. </span><em>Pablo Loyola, Edison Marrese-Taylor and Yutaka Matsuo</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">English Event Detection With Translated Language Features. </span><em>Sam Wei, Igor Korostil, Joel Nothman and Ben Hachey</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">EviNets: Evidence Neural Networks for Combining Evidence Signals for Factoid Question Answering. </span><em>Denis Savenkov and Eugene Agichtein</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Pocket Knowledge Base Population. </span><em>Travis Wolfe, Mark Dredze and Benjamin Van Durme</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Complex Question Answering by Reasoning over Open Information Extraction. </span><em>Tushar Khot, Ashish Sabharwal and Peter Clark</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bootstrapping for Numerical Open IE. </span><em>Swarnadeep Saha, Harinder Pal and Mausam</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Feature-Rich Deep Neural Networks for Knowledge Base Completion. </span><em>Alexandros Komninos and Suresh Manandhar</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Fine-Grained Entity Typing with High-Multiplicity Assignments. </span><em>Maxim Rabinovich and Dan Klein</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Group Sparse CNNs for Question Classification with Answer Sets. </span><em>Mingbo Ma, Liang Huang, Bing Xiang and Bowen Zhou</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Multi-Task Learning of Keyphrase Boundary Classification. </span><em>Isabelle Augenstein and Anders Søgaard</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cardinal Virtues: Extracting Relation Cardinalities from Text. </span><em>Paramita Mirza, Simon Razniewski, Fariz Darari and Gerhard Weikum</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Integrating Deep Linguistic Features in Factuality Prediction over Unified Datasets. </span><em>Gabriel Stanovsky, Judith Eckle-Kohler, Yevgeniy Puzikov, Ido Dagan and Iryna Gurevych</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Question Answering with Universal Schema and Memory Networks. </span><em>Rajarshi Das, Manzil Zaheer, Siva Reddy and Andrew McCallum</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Differentiable Scheduled Sampling for Credit Assignment. </span><em>Kartik Goyal, Chris Dyer and Taylor Berg-Kirkpatrick</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Deep Network with Visual Text Composition Behavior. </span><em>Hongyu GUO</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Neural System Combination for Machine Translation. </span><em>Long Zhou, Wenpeng Hu, Jiajun Zhang and Chengqing Zong</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">An Empirical Comparison of Domain Adaptation Methods for Neural Machine Translation. </span><em>Chenhui Chu, Raj Dabre and Sadao Kurohashi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Efficient Extraction of Pseudo-Parallel Sentences from Raw Monolingual Data Using Word Embeddings. </span><em>Benjamin Marie and Atsushi Fujita</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Feature Hashing for Language and Dialect Identification. </span><em>Shervin Malmasi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Detection of Chinese Word Usage Errors for Non-Native Chinese Learners with Bidirectional LSTM. </span><em>Yow-Ting Shiue, Hen-Hsen Huang and Hsin-Hsi Chen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatic Compositor Attribution in the First Folio of Shakespeare. </span><em>Maria Ryskina, Hannah Alpert-Abrams, Dan Garrette and Taylor Berg-Kirkpatrick</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Constructing Large-Scale Japanese Image Caption Dataset. </span><em>Yuya Yoshikawa, Yutaro Shigeto and Akikazu Takeuchi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">“Liar, Liar Pants on Fire”: A New Benchmark Dataset for Fake News Detection. </span><em>William Yang Wang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">English Multiword Expression-aware Dependency Parsing including Named Entities. </span><em>Akihiko Kato, Hiroyuki Shindo and Yuji Matsumoto</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving Semantic Composition with Offset Inference. </span><em>Thomas Kober, Julie Weeds, Jeremy Reffin and David Weir</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Topic-Sensitive Word Representations. </span><em>Marzieh Fadaee, Arianna Bisazza and Christof Monz</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Temporal Word Analogies: Identifying Lexical Replacement with Diachronic Word Embeddings. </span><em>Terrence Szymanski</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Methodical Evaluation of Arabic Word Embeddings. </span><em>Mohammed Elrazzaz, Chadi Helwe, Shady Elbassuoni and Khaled Shaban</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Multilingual Connotation Frames: A Case Study on Social Media for Targeted Sentiment Analysis and Forecast. </span><em>Hannah Rashkin, Eric Bell, Yejin Choi and Svitlana Volkova</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Best-Worst Scaling More Reliable than Rating Scales: A Case Study on Sentiment Intensity Annotation. </span><em>Svetlana Kiritchenko and Saif Mohammad</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Demographic Inference on Twitter using Recursive Neural Networks. </span><em>Sunghwan Mac Kim, Qiongkai Xu, Lizhen Qu and Stephen Wan</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Twitter Demographic Classification using deep Multi-modal Multi-task Learning. </span><em>Soroush Vosoughi, Prashanth Vijayaraghavan and Deb Roy</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Network Framework for Noisy Label Aggregation in Social Media. </span><em>Xueying Zhan, Yaowei Wang, Yanghui Rao, Haoran Xie, Qing Li, Fu Lee Wang and Tak-Lam Wong</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Parser Adaptation for Social Media by Integrating Normalization. </span><em>Rob van der Goot and Gertjan van Noord</em>
                    </td>
                </tr>
            </table>
            <h4 class="poster-type" style="text-decoration: underline;">Student Research Workshop</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Computational Characterization of Mental States: A Natural Language Processing Approach. </span><em>Facundo Carrillo</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving Distributed Representations of Tweets - Present and Future. </span><em>Ganesh Jawahar</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bilingual Word Embeddings with Bucketed CNN for Parallel Sentence Extraction. </span><em>Jeenu Grover and Pabitra Mitra</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">nQuery - A Natural Language Statement to SQL Query Generator. </span><em>Nandan Sukthankar, Sanket Maharnawar, Pranay Deshmukh, Yashodhara Haribhakta and Vibhavari Kamble</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">V for Vocab : An Intelligent Flashcard Application. </span><em>Nihal V. Nayak, Tanmay Chinchore, Aishwarya Hanumanth Rao, Shane Michael Martin, Sagar Nagaraj Simha, G. M. Lingaraju and H. S. Jamadagni</em>
                    </td>
                </tr>                
                <tr id="poster">
                    <td>
                        <span class="poster-title">Are You Asking the Right Questions? Teaching Machines to Ask Clarification Questions. </span><em>Sudha Rao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Building a Non-Trivial Paraphrase Corpus Using Multiple Machine Translation Systems. </span><em>Yui Suzuki, Tomoyuki Kajiwara and Mamoru Komachi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Segmentation Guided Attention Networks for Visual Question Answering. </span><em>Vasu Sharma, Ankita Bishnu and Labhesh Patel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Text-based Speaker Identification on Multiparty Dialogues Using Multi-document Convolutional Neural Networks. </span><em>Kaixin Ma, Catherine Xiao and Jinho D. Choi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Variation Autoencoder Based Network Representation Learning for Classification. </span><em>Hang Li, Haozheng Wang, Zhenglu Yang and Masato Odagaki</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Blind Phoneme Segmentation With Temporal Prediction Errors. </span><em>Paul Michel, Okko Räsänen, Roland Thiolliere and Emmanuel Dupoux</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatic Generation of Jokes in Hindi. </span><em>Srishti Aggarwal and Radhika Mamidi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Word Embedding for Response-To-Text Assessment of Evidence. </span><em>Haoran Zhang and Diane Litman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Domain Specific Automatic Question Generation from Text. </span><em>Katira Soleymanzadeh</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">SoccEval: An Annotation Schema for Rating Soccer Players. </span><em>Jose Ramirez, Matthew Garber and Xinhao Wang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Accent Adaptation for the Air Traffic Control Domain. </span><em>Matthew Garber, Meital Singer and Christopher Ward</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Generating Steganographic Text with LSTMs. </span><em>Tina Fang, Martin Jaggi and Katerina Argyraki</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Predicting Depression for Japanese Blog Text. </span><em>Misato Hiraga</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Fast Forward Through Opportunistic Incremental Meaning Representation Construction. </span><em>Petr Babkin and Sergei Nirenburg</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Modeling Situations in Neural Chat Bots. </span><em>Shoetsu Sato, Naoki Yoshinaga, Masashi Toyoda and Masaru Kitsuregawa</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">An Empirical Study on End-to-End Sentence Modelling. </span><em>Kurt Junshean Espinosa</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Varying Linguistic Purposes of Emoji in (Twitter) Context. </span><em>Noa Naaman, Hannah Provenza and Orion Montoya</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Negotiation of Antibiotic Treatment in Medical Consultations: A Corpus Based Study. </span><em>Nan Wang</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="day" id="third-day">Tuesday, August 1</div>
    <div class="session session-plenary" id="session-breakfast-2">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-invited-noah">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: Squashing Computational Linguistics</a><br/>        
        <span class="session-people">Noah Smith (University of Washington)</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:10 AM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grand Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>The computational linguistics and natural language processing community is experiencing an episode of deep fascination with representation learning.  Like many other presenters at this conference, I will describe new ways to use representation learning in models of natural language.  Noting that a data-driven model always assumes a theory (not necessarily a good one), I will argue for the benefits of language-appropriate inductive bias for representation-learning-infused models of language.  Such bias often comes in the form of assumptions baked into a model, constraints on an inference algorithm, or linguistic analysis applied to data.  Indeed, many decades of research in linguistics (including computational linguistics) put our community in a strong position to identify promising inductive biases.  The new models, in turn, may allow us to explore previously unavailable forms of bias, and to produce findings of interest to linguistics.  I will focus on new models of documents and of sentential semantic structures, and I will emphasize abstract, reusable components and their assumptions rather than applications.</p>
            </div>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-3">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:10 AM &ndash; 10:30 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-4a">
        <div id="expander"></div><a href="#" class="session-title">Information Extraction 3</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:05 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="76">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Deep Pyramid Convolutional Neural Networks for Text Categorization. </span><em>Rie Johnson and Tong Zhang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="77">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Improved Neural Relation Detection for Knowledge Base Question Answering. </span><em>Mo Yu, Wenpeng Yin, Kazi Saidul Hasan, Cicero dos Santos, Bing Xiang and Bowen Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="78">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Deep Keyphrase Generation. </span><em>Rui Meng, Daqing He, Sanqiang Zhao and Shuguang Han</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="79">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Attention-over-Attention Neural Networks for Reading Comprehension. </span><em>Yiming Cui, Zhipeng Chen, Si wei, Shijin Wang, Ting Liu and Guoping Hu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="80">
                        <td id="paper-time">11:46-12:04</td>
                        <td>
                            <span class="paper-title">Cross-Sentence N-ary Relation Extraction with Graph LSTMs. </span><em>Nanyun Peng, Hoifung Poon, Chris Quirk, Kristina Toutanova, Wen-Tau Yih</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-4b">
        <div id="expander"></div><a href="#" class="session-title">Vision 2</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:05 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="81">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Alignment at Work: Using Language to Distinguish the Internalization and Self-Regulation Components of Cultural Fit in Organizations. </span><em>Gabriel Doyle, Amir Goldberg, Sameer Srivastava and Michael Frank</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="82">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Representations of language in a model of visually grounded speech signal. </span><em>Grzegorz Chrupała, Lieke Gelderloos and Afra Alishahi</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="83">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Spectral Analysis of Information Density in Dialogue Predicts Collaborative Task Performance. </span><em>Yang Xu and David Reitter</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="84">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Modeling Semantic Expectation: Using Script Knowledge for Referent Prediction. </span><em>Ashutosh Modi, Ivan Titov, Vera Demberg, Asad Sayeed, Manfred Pinkal</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="85">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">A Survey on Action Recognition Datasets and Tasks for Still Images. </span><em>Spandana Gella and Frank Keller</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-4c">
        <div id="expander"></div><a href="#" class="session-title">Dialogue 2</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:05 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="86">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Affect-LM: A Neural Language Model for Customizable Affective Text Generation. </span><em>Sayan Ghosh, Mathieu Chollet, Eugene Laksana, Stefan Scherer and Louis-Philippe Morency</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="87">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Domain Attention with an Ensemble of Experts. </span><em>Young-Bum Kim, Karl Stratos and Dongchan Kim</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="88">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Learning Discourse-level Diversity for Neural Dialog Models using Conditional Variational Autoencoders. </span><em>Tiancheng Zhao, Ran Zhao and Maxine Eskenazi</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="89">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Hybrid Code Networks: practical and efficient end-to-end dialog control with supervised and reinforcement learning. </span><em>Jason D Williams, Kavosh Asadi and Geoffrey Zweig</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="90">
                        <td id="paper-time">11:46-12:04</td>
                        <td>
                            <span class="paper-title">Generating Contrastive Referring Expressions. </span><em>Martin Villalba, Christoph Teichmann and Alexander Koller</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-4d">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation 2</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:05 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="91">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Modeling Source Syntax for Neural Machine Translation. </span><em>Junhui Li, Deyi Xiong, Zhaopeng Tu, Muhua Zhu and Guodong Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="92">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Sequence-to-Dependency Neural Machine Translation. </span><em>Shuangzhi Wu, Dongdong Zhang, Nan Yang, Mu Li and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="93">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Head-Lexicalized Bidirectional Tree LSTMs. </span><em>Zhiyang Teng and Yue Zhang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="94">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Pushing the Limits of Translation Quality Estimation. </span><em>André F. T. Martins, Marcin Junczys-Dowmunt, Fabio N. Kepler, Ramón Astudillo, Chris Hokamp, Roman Grundkiewicz</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="95">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">Learning to Parse and Translate Improves Neural Machine Translation. </span><em>Akiko Eriguchi, Yoshimasa Tsuruoka and Kyunghyun Cho</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-4e">
        <div id="expander"></div><a href="#" class="session-title">Social Media</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:05 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="96">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Detect Rumors in Microblog Posts Using Propagation Structure via Kernel Learning. </span><em>Ma Jing, Wei Gao and Kam-Fai Wong</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="97">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">EmoNet: Fine-Grained Emotion Detection with Gated Recurrent Neural Networks. </span><em>Muhammad Abdul-Mageed and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="98">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Beyond Binary Labels: Political Ideology Prediction of Twitter Users. </span><em>Daniel Preoţiuc-Pietro, Ye Liu, Daniel Hopkins and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="99">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Leveraging Behavioral and Social Information for Weakly Supervised Collective Classification of Political Discourse on Twitter. </span><em>Kristen Johnson and Dan Goldwasser</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="100">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">On the Distribution of Lexical Features in Social Media. </span><em>Fatemeh Almodaresi, Lyle Ungar, Vivek Kulkarni, Mohsen Zakeri, Salvatore Giorgi and H. Andrew Schwartz</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>    
    <div class="session session-plenary" id="session-lunch-arxiv">
        <span class="session-title">Bring Lunch and Discuss: Double Blind Reviewing &amp; arXiv</span><br/>
        <span class="session-time">12:05 PM &ndash; 1:30 PM</span><br/>
        <span class="session-location btn btn--location">Salons E/F</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-5a">
        <div id="expander"></div><a href="#" class="session-title">Multidisciplinary</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="101">
                        <td id="paper-time">1:30-1:42</td>
                        <td>
                            <span class="paper-title">Exploring Neural Text Simplification Models. </span><em>Sergiu Nisioi, Sanja Štajner, Simone Paolo Ponzetto and Liviu P. Dinu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="102">
                        <td id="paper-time">1:43-2:01</td>
                        <td>
                            <span class="paper-title">A Nested Attention Neural Hybrid Model for Grammatical Error Correction. </span><em>Jianshu Ji, Qinlong Wang, Kristina Toutanova, Yongen Gong, Steven Truong and Jianfeng Gao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="103">
                        <td id="paper-time">2:02-2:20</td>
                        <td>
                            <span class="paper-title">TextFlow: A Text Similarity Measure based on Continuous Sequences. </span><em>Yassine Mrabet, Halil Kilicoglu and Dina Demner-Fushman</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="104">
                        <td id="paper-time">2:21-2:39</td>
                        <td>
                            <span class="paper-title">Friendships, Rivalries, and Trysts: Characterizing Relations between Ideas in Texts. </span><em>Chenhao Tan, Dallas Card and Noah A. Smith</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="105">
                        <td id="paper-time">2:40-2:52</td>
                        <td>
                            <span class="paper-title">On the Challenges of Translating NLP Research into Commercial Products. </span><em>Daniel Dahlmeier</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-5b">
        <div id="expander"></div><a href="#" class="session-title">Languages &amp; Resources</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="106">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Polish evaluation dataset for compositional distributional semantics models. </span><em>Alina Wróblewska and Katarzyna Krasnowska-Kieraś</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="107">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction. </span><em>Christopher Bryant, Mariano Felice and Ted Briscoe</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="108">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Evaluation Metrics for Reading Comprehension: Prerequisite Skills and Readability. </span><em>Saku Sugawara, Yusuke Kido, Hikaru Yokono and Akiko Aizawa</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="109">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Sentence Alignment Methods for Improving Text Simplification Systems. </span><em>Sanja Štajner, Marc Franco-Salvador, Simone Paolo Ponzetto, Paolo Rosso and Heiner Stuckenschmidt</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="110">
                        <td id="paper-time">2:40-2:52</td>
                        <td>
                            <span class="paper-title">Understanding Task Design Trade-offs in Crowdsourced Paraphrase Collection. </span><em>Youxuan Jiang, Jonathan K. Kummerfeld and Walter S. Lasecki</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-5c">
        <div id="expander"></div><a href="#" class="session-title">Syntax 2</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="111">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">A Minimal Span-Based Neural Constituent Parser. </span><em>Mitchell Stern, Jacob Andreas and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="112">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">Semantic Dependency Parsing via Book Embedding. </span><em>Weiwei Sun, Junjie Cao and Xiaojun Wan</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="113">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Neural Word Segmentation with Rich Pretraining. </span><em>Jie Yang, Yue Zhang and Fei Dong</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="114">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Arc-swift: A Novel Transition System for Dependency Parsing. </span><em>Peng Qi and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="115">
                        <td id="paper-time">2:40-2:52</td>
                        <td>
                            <span class="paper-title">A Generative Parser with a Discriminative Recognition Algorithm. </span><em>Jianpeng Cheng, Adam Lopez and Mirella Lapata</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-5d">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation 3</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="116">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Neural Machine Translation via Binary Code Prediction. </span><em>Yusuke Oda, Philip Arthur, Graham Neubig, Koichiro Yoshino and Satoshi Nakamura</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="117">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">What do Neural Machine Translation Models Learn about Morphology?. </span><em>Yonatan Belinkov, Nadir Durrani, Fahim Dalvi, Hassan Sajjad and James Glass</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="118">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Fully Character-Level Neural Machine Translation without Explicit Segmentation. </span><em>Jason Lee, Kyunghyun Cho, Thomas Hofmann</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="119">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Hybrid Neural Network Alignment and Lexicon Model in Direct HMM for Statistical Machine Translation. </span><em>Weiyue Wang, Derui Zhu and Hermann Ney</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="120">
                        <td id="paper-time">2:40-2:52</td>
                        <td>
                            <span class="paper-title">Towards String-To-Tree Neural Machine Translation. </span><em>Roee Aharoni and Yoav Goldberg</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-5e">
        <div id="expander"></div><a href="#" class="session-title">Sentiment 2</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="121">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Modeling Contextual Relationship Among Utterances in Multimodal Sentiment Analysis. </span><em>Soujanya Poria, Devamanyu Hazarika, Navonil Majumder and Erik Cambria</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="122">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">A Multidimensional Lexicon for Interpersonal Stancetaking. </span><em>Umashanthi Pavalanathan, Jim Fitzpatrick, Scott Kiesling and Jacob Eisenstein</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="123">
                        <td id="paper-time">2:08-2:20</td>
                        <td>
                            <span class="paper-title">Learning Lexical-Functional Patterns for First-Person Affect. </span><em>Lena Reed, Jiaqi Wu, Shereen Oraby, Pranav Anand and Marilyn Walker</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="124">
                        <td id="paper-time">2:21-2:33</td>
                        <td>
                            <span class="paper-title">Supervised Aspect Extraction with Knowledge Retention. </span><em>Lei Shu, Hu Xu and Bing Liu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="125">
                        <td id="paper-time">2:34-2:46</td>
                        <td>
                            <span class="paper-title">Exploiting Domain Knowledge via Grouped Weight Sharing with Application to Text Categorization. </span><em>Ye Zhang, Matthew Lease and Byron C. Wallace</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-plenary" id="session-break-4">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:05 PM &ndash; 3:25 PM</span>
    </div>    
    <div class="session session-expandable session-papers1" id="session-6a">
        <div id="expander"></div><a href="#" class="session-title">Information Extraction 4</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="126">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Tandem Anchoring: a Multiword Anchor Approach for Interactive Topic Modeling. </span><em>Jeffrey Lund, Connor Cook, Kevin Seppi and Jordan Boyd-Graber</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="127">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Comparing Apples to Apples: Learning Semantics of Common Entities Through a Novel Comprehension Task. </span><em>Omid Bakhshandeh and James Allen</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="128">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Going out on a limb : Joint Extraction of Entity Mentions and Relations without Dependency Trees. </span><em>Arzoo Katiyar and Claire Cardie</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="129">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Evaluating Visual Representations for Topic Understanding and Their Effects on Manually Generated Labels. </span><em>Alison Smith, Tak Yeon Lee, Forough-Poursabzi Sangdeh, Jordan Boyd-Graber, Niklas Elmqvist, Leah Findlater</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="130">
                        <td id="paper-time">4:41-4:53</td>
                        <td>
                            <span class="paper-title">Separating Reranking Effects from Model Combination Effects in Generative Neural Constituency Parsers. </span><em>Daniel Fried, Mitchell Stern and Dan Klein</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-6b">
        <div id="expander"></div><a href="#" class="session-title">Semantics 3</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="131">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Naturalizing a Programming Language via Interactive Learning. </span><em>Sida I. Wang, Sam Ginn, Percy Liang and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="132">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Semantic Word Clusters Using Signed Spectral Clustering. </span><em>Joao Sedoc, Jean Gallier, Dean Foster and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="133">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">An Interpretable Knowledge Transfer Model for Knowledge Base Completion. </span><em>Qizhe Xie, Xuezhe Ma, Zihang Dai and Eduard Hovy</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="134">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Learning a Neural Semantic Parser from User Feedback. </span><em>Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, Jayant Krishnamurthy and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="135">
                        <td id="paper-time">4:41-4:59</td>
                        <td>
                            <span class="paper-title">Enriching Word Vectors with Subword Information. </span><em>Piotr Bojanowski, Edouard Grave, Armand Joulin and Tomas Mikolov</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers3" id="session-6c">
        <div id="expander"></div><a href="#" class="session-title">Discourse 2 / Dialogue 3</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon D</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="136">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Joint Modeling of Content and Discourse Relations in Dialogues. </span><em>Kechen Qin, Lu Wang, Joseph Kim and Julie Shah</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="137">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Argument Mining with Structured SVMs and RNNs. </span><em>Vlad Niculae, Claire Cardie and Joonsuk Park</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="138">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Neural Discourse Structure for Text Categorization. </span><em>Yangfeng Ji and Noah A. Smith</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="139">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Adversarial Connective-exploiting Networks for Implicit Discourse Relation Classification. </span><em>Lianhui Qin, Zhisong Zhang, Hai Zhao, Eric Xing and Zhiting Hu</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="140">
                        <td id="paper-time">4:41-4:59</td>
                        <td>
                            <span class="paper-title">Don’t understand a measure? Learn it: Structured Prediction for Coreference Resolution optimizing its measures. </span><em>Iryna Haponchyk and Alessandro Moschitti</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers4" id="session-6d">
        <div id="expander"></div><a href="#" class="session-title">Machine Learning 2</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salon 1</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="141">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Bayesian Modeling of Lexical Resources for Low-Resource Settings. </span><em>Nicholas Andrews, Jason Eisner, Mark Dredze and Benjamin Van Durme</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="142">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Semi-Supervised QA with Generative Domain-Adaptive Nets. </span><em>Zhilin Yang, Junjie Hu, Ruslan Salakhutdinov and William Cohen</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="143">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">From Language to Programs: Bridging Reinforcement Learning and Maximum Marginal Likelihood. </span><em>Kelvin Guu, Panupong Pasupat, Evan Liu and Percy Liang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="144">
                        <td id="paper-time">4:22-4:34</td>
                        <td>
                            <span class="paper-title">Information-Theory Interpretation of the Skip-Gram Negative-Sampling Objective Function. </span><em>Oren Melamud and Jacob Goldberger</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="145">
                        <td id="paper-time">4:35-4:47</td>
                        <td>
                            <span class="paper-title">Implicitly-Defined Neural Networks for Sequence Labeling. </span><em>Michaeel Kazi and Brian Thompson</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-6e">
        <div id="expander"></div><a href="#" class="session-title">Summarization</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons 2/3</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="146">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Diversity driven attention model for query-based abstractive summarization. </span><em>Preksha Nema, Mitesh M. Khapra, Balaraman Ravindran and Anirban Laha</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="147">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Get To The Point: Summarization with Pointer-Generator Networks. </span><em>Abigail See, Peter J. Liu and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="148">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Supervised Learning of Automatic Pyramid for Optimization-Based Multi-Document Summarization. </span><em>Maxime Peyrard and Judith Eckle-Kohler</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="149">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Selective Encoding for Abstractive Sentence Summarization. </span><em>Qingyu Zhou, Nan Yang, Furu Wei and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="150">
                        <td id="paper-time">4:41-4:59</td>
                        <td>
                            <span class="paper-title">PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents. </span><em>Corina Florescu and Cornelia Caragea</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-posters" id="session-poster-2">
        <div id="expander"></div><a href="#" class="session-title">Posters, Demos &amp; Dinner</a><br/>        
        <span class="session-time">5:45 PM &ndash; 7:45 PM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grand Foyer/Stanley Park Foyer/Cypress</span>
        <div class="poster-session-details">
            <hr class="detail-separator"/>
            <h4 class="poster-type" style="text-decoration: underline;">Long Papers</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Symmetric Collaborative Dialogue Agents with Dynamic Knowledge Graph Embeddings. </span><em>He He, Anusha Balakrishnan, Mihail Eric and Percy Liang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Neural Belief Tracker: Data-Driven Dialogue State Tracking. </span><em>Nikola Mrkšić, Diarmuid Ó Séaghdha, Tsung-Hsien Wen, Blaise Thomson and Steve Young</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Exploiting Argument Information to Improve Event Detection via Supervised Attention Mechanisms. </span><em>Shulin Liu, Kang Liu and Jun Zhao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Topical Coherence in LDA-based Models through Induced Segmentation. </span><em>Hesam Amoualian, Wei Lu, Eric Gaussier, Massih R Amini, Georgios Balikas and Marianne Clausel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Joint Extraction of Relations with Class Ties via Effective Deep Ranking. </span><em>Hai Ye, Wenhan Chao and Zhunchen Luo</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Search-based Neural Structured Learning for Sequential Question Answering. </span><em>Mohit Iyyer, Wen-tau Yih and Ming-Wei Chang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Gated-Attention Readers for Text Comprehension. </span><em>Bhuwan Dhingra, Hanxiao Liu, Zhilin Yang, William Cohen and Ruslan Salakhutdinov</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Determining Gains Acquired from Word Embedding Quantitatively using Discrete Distribution Clustering. </span><em>Jianbo Ye, Yanran Li, Zhaohui Wu, James Z. Wang and Jia Li</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Towards a Seamless Integration of Word Senses into Downstream NLP Applications. </span><em>Mohammad Taher Pilehvar, Jose Camacho-Collados, Roberto Navigli and Nigel Collier</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Reading Wikipedia to Answer Open-Domain Questions. </span><em>Danqi Chen, Adam Fisch, Jason Weston and Antoine Bordes</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Skim Text. </span><em>Adams Wei Yu, Quoc Le and Hongrae Lee</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">An Algebra for Feature Extraction. </span><em>Vivek Srikumar</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Chunk-based Decoder for Neural Machine Translation. </span><em>Shonosuke Ishiwatari, Jingtao Yao, Shujie Liu, Mu Li, Ming Zhou, Naoki Yoshinaga, Masaru Kitsuregawa and Weijia Jia</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Doubly-Attentive Decoder for Multi-modal Neural Machine Translation. </span><em>Iacer Calixto, Qun Liu and Nick Campbell</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Teacher-Student Framework for Zero-Resource Neural Machine Translation. </span><em>Yun Chen, Yang Liu, Yong Cheng and Victor O.K. Li</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improved Neural Machine Translation with a Syntax-Aware Encoder and Decoder. </span><em>Huadong Chen, Shujian Huang, David Chiang and Jiajun Chen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-lingual Name Tagging and Linking for 282 Languages. </span><em>Xiaoman Pan, Boliang Zhang, Jonathan May, Joel Nothman, Kevin Knight and Heng Ji</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Adversarial Training for Unsupervised Bilingual Lexicon Induction. </span><em>Meng Zhang, Yang Liu, Huanbo Luan and Maosong Sun</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Estimating Code-Switching on Twitter with a Novel Generalized Word-Level Language Detection Technique. </span><em>Shruti Rijhwani, Royal Sequiera, Monojit Choudhury, Kalika Bali and Chandra Shekhar Maddila</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Using Global Constraints and Reranking to Improve Cognates Detection. </span><em>Michael Bloodgood and Benjamin Strauss</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">One-Shot Neural Cross-Lingual Transfer for Paradigm Completion. </span><em>Katharina Kann, Ryan Cotterell and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Morphological Inflection Generation with Hard Monotonic Attention. </span><em>Roee Aharoni and Yoav Goldberg</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">From Characters to Words to in Between: Do We Capture Morphology?. </span><em>Clara Vania and Adam Lopez</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Riemannian Optimization for Skip-Gram Negative Sampling. </span><em>Alexander Fonarev, Oleksii Hrinchuk, Gleb Gusev, Pavel Serdyukov and Ivan Oseledets</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Deep Multitask Learning for Semantic Dependency Parsing. </span><em>Hao Peng, Sam Thomson and Noah A. Smith</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improved Word Representation Learning with Sememes. </span><em>Yilin Niu, Ruobing Xie, Zhiyuan Liu and Maosong Sun</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Character-level Compositionality with Visual Features. </span><em>Frederick Liu, Han Lu, Chieh Lo and Graham Neubig</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Progressive Learning Approach to Chinese SRL Using Heterogeneous Data. </span><em>Qiaolin Xia, Zhifang Sui and Baobao Chang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Revisiting Recurrent Networks for Paraphrastic Sentence Embeddings. </span><em>John Wieting and Kevin Gimpel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Using Ontology-Grounded Token Embeddings To Predict Prepositional Phrase Attachments. </span><em>Pradeep Dasigi, Waleed Ammar, Chris Dyer and Eduard Hovy</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Identifying 1950s American Jazz Composers: Fine-Grained IsA Extraction via Modifier Composition. </span><em>Ellie Pavlick and Marius Pasca</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Parsing to 1-Endpoint-Crossing, Pagenumber-2 Graphs. </span><em>Junjie Cao, Sheng Huang, Weiwei Sun and Xiaojun Wan</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Semi-supervised Multitask Learning for Sequence Labeling. </span><em>Marek Rei</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Semantic Parsing of Pre-university Math Problems. </span><em>Takuya Matsuzaki, Takumi Ito, Hidenao Iwane, Hirokazu Anai and Noriko H. Arai</em>
                    </td>
                </tr>
            </table>
            <h4 class="poster-type" style="text-decoration: underline;">Short Papers</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">MeChat: A Sequence to Sequence and Rerank based Chatbot Engine. </span><em>Minghui Qiu and Feng-Lin Li</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Conditional Variational Framework for Dialog Generation. </span><em>Xiaoyu Shen, Hui Su, Yanran Li, Wenjie Li, Shuzi Niu and Akiko Aizawa</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Question Answering through Transfer Learning from Large Fine-grained Supervision Data. </span><em>Sewon Min, Minjoon Seo and Hannaneh Hajishirzi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Self-Crowdsourcing Training for Relation Extraction. </span><em>Azad Abad, Moin Nabi and Alessandro Moschitti</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Generative Attentional Neural Network Model for Dialogue Act Classification. </span><em>Quan Hung Tran, Gholamreza Haffari and Ingrid Zukerman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Salience Rank: Efficient Keyphrase Extraction with Topic Modeling. </span><em>Nedelina Teneva and Weiwei Cheng</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">List-only Entity Linking. </span><em>Ying Lin, Chin-Yew Lin and Heng Ji</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving Native Language Identification by Using Spelling Errors. </span><em>Lingzhen Chen, Carlo Strapparava and Vivi Nastase</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Disfluency Detection using a Noisy Channel Model and a Deep Neural Language Model. </span><em>Paria Jamshid Lou and Mark Johnson</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">On the Equivalence of Holographic and Complex Embeddings for Knowledge Graph Completion. </span><em>Katsuhiko Hayashi and Masashi Shimbo</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sentence Embedding for Neural Machine Translation Domain Adaptation. </span><em>Rui Wang, Andrew Finch, Masao Utiyama and Eiichiro Sumita</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Data Augmentation for Low-Resource Neural Machine Translation. </span><em>Marzieh Fadaee, Arianna Bisazza and Christof Monz</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Speeding up Neural Machine Translation Decoding by Shrinking Run-time Vocabulary. </span><em>Xing Shi and Kevin Knight</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Chunk-Based Bi-Scale Decoder for Neural Machine Translation. </span><em>Hao Zhou, Zhaopeng Tu, Shujian Huang, Xiaohua Liu, Hang Li and Jiajun Chen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Model Transfer for Tagging Low-resource Languages without Bilingual Corpora. </span><em>Meng Fang and Trevor Cohn</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">EuroSense: Automatic Harvesting of Multilingual Sense Annotations from Parallel Text. </span><em>Claudio Delli Bovi, Jose Camacho-Collados, Alessandro Raganato and Roberto Navigli</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Challenging Language-Dependent Segmentation for Arabic: An Application to Machine Translation and Part-of-Speech Tagging. </span><em>Hassan Sajjad, Fahim Dalvi, Nadir Durrani, Ahmed Abdelali, Yonatan Belinkov and Stephan Vogel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Fast and Accurate Neural Word Segmentation. </span><em>Deng Cai and Hai Zhao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">The Value of Curated Negative Examples: Strong Baselines for Story Cloze Tasks. </span><em>Zheng Cai, Lifu Tu and Kevin Gimpel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Neural Semantic Parsing over Multiple Knowledge-bases. </span><em>Jonathan Herzig and Jonathan Berant</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Geometry of Sentences. </span><em>Jiaqi Mu, Suma Bhat and Pramod Viswanath</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving Semantic Relevance for Chinese Social Media Text Summarization. </span><em>Shuming Ma and Xu Sun</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Determining Whether and When People Participate in the Events They Tweet About. </span><em>Krishna Sanagavarapu, Alakananda Vempala and Eduardo Blanco</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Separating Facts from Fiction: Linguistic Models to Classify Suspicious and Trusted News Posts on Twitter. </span><em>Kyle Shaffer, Jin Yea Jang, Nathan Hodas and Svitlana Volkova</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Recognizing Counterfactual Thinking in Social Media Texts. </span><em>Youngseo Son, Anneke Buffone, H. Andrew Schwartz and Lyle Ungar</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Temporal Orientation of Tweets for Predicting Income of User. </span><em>Mohammed Hasanuzzaman, Sabyasachi Kamila, Mandeep Kaur, Sriparna Saha and Asif Ekbal</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Character-Aware Neural Morphological Disambiguation. </span><em>Alymzhan Toleu, Gulmira Tolegen and Aibek Makazhanov</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Character Composition Model with Convolutional Neural Networks for Dependency Parsing on Morphologically Rich Languages. </span><em>Xiang Yu and Ngoc Thang Vu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">How (not) to train a dependency parser: The curious case of jackknifing part-of-speech taggers. </span><em>Željko Agić and Natalie Schluter</em>
                    </td>
                </tr>
            </table>
            <h4 class="poster-type" style="text-decoration: underline;">System Demonstrations</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Annotating tense, mood and voice for English, French and German. </span><em>Anita Ramm, Sharid Loáiciga, Annemarie Friedrich and Alexander Fraser</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automating Biomedical Evidence Synthesis: RobotReviewer. </span><em>Iain Marshall, Joël Kuiper, Edward Banner and Byron C. Wallace</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Benben: A Chinese Intelligent Conversational Robot. </span><em>Wei-Nan Zhang, Ting Liu, Bing Qin, Yu Zhang, Wanxiang Che, Yanyan Zhao and Xiao Ding</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">End-to-End Non-Factoid Question Answering with an Interactive Visualization of Neural Attention Weights. </span><em>Andreas Rücklé and Iryna Gurevych</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">ESTEEM: A Novel Framework for Qualitatively Evaluating and Visualizing Spatiotemporal Embeddings in Social Media. </span><em>Dustin Arendt and Svitlana Volkova</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Exploring Diachronic Lexical Semantics with JeSemE. </span><em>Johannes Hellrich and Udo Hahn</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Extended Named Entity Recognition API and Its Applications in Language Education. </span><em>Tuan Duc Nguyen, Khai Mai, Thai-Hoang Pham, Minh Trung Nguyen, Truc-Vien T. Nguyen, Takashi Eguchi, Ryohei Sasano and Satoshi Sekine</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Hafez: an Interactive Poetry Generation System. </span><em>Marjan Ghazvininejad, Xing Shi, Jay Priyadarshi and Kevin Knight</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Interactive Visual Analysis of Transcribed Multi-Party Discourse. </span><em>Mennatallah El-Assady, Annette Hautli-Janisz, Valentin Gold, Miriam Butt, Katharina Holzinger and Daniel Keim</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Life-iNet: A Structured Network-Based Knowledge Exploration and Analytics System for Life Sciences. </span><em>Xiang Ren, Jiaming Shen, Meng Qu, Xuan Wang, Zeqiu Wu, Qi Zhu, Meng Jiang, Fangbo Tao, Saurabh Sinha, David Liem, Peipei Ping, Richard Weinshilboum and Jiawei Han</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Olelo: A Question Answering Application for Biomedicine. </span><em>Mariana Neves, Hendrik Folkerts, Marcel Jankrift, Julian Niedermeier, Toni Stachewicz, Sören Tietböhl, Milena Kraus and Matthias Uflacker</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">OpenNMT: Open-Source Toolkit for Neural Machine Translation. </span><em>Guillaume Klein, Yoon Kim, Yuntian Deng, Jean Senellart and Alexander Rush</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">PyDial: A Multi-domain Statistical Dialogue System Toolkit. </span><em>Stefan Ultes, Lina M. Rojas Barahona, Pei-Hao Su, David Vandyke, Dongho Kim, Iñigo Casanueva, Paweł Budzianowski, Nikola Mrkšić, Tsung-Hsien Wen, Milica Gasic and Steve Young</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">RelTextRank: An Open Source Framework for Building Relational Syntactic-Semantic Text Pair Representations. </span><em>Kateryna Tymoshenko, Alessandro Moschitti, Massimo Nicosia and Aliaksei Severyn</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Scattertext: a Browser-Based Tool for Visualizing how Corpora Differ. </span><em>Jason Kessler</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Semedico: A Comprehensive Semantic Search Engine for the Life Sciences. </span><em>Erik Faessler and Udo Hahn</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">SuperAgent: A Customer Service Chatbot for E-commerce Websites. </span><em>Lei Cui, Shaohan Huang, Furu Wei, Chuanqi Tan, Chaoqun Duan and Ming Zhou</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Swanson linking revisited: Accelerating literature-based discovery across domains using a conceptual influence graph. </span><em>Gus Hahn-Powell, Marco A. Valenzuela-Escárcega and Mihai Surdeanu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">UCCAApp: Web-application for Syntactic and Semantic Phrase-based Annotation. </span><em>Omri Abend, Shai Yerushalmi and Ari Rappoport</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">WebChild 2.0 : Fine-Grained Commonsense Knowledge Distillation. </span><em>Niket Tandon, Gerard de Melo and Gerhard Weikum</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Zara Returns: Improved Personality Induction and Adaptation by an Empathetic Virtual Agent. </span><em>Farhad Bin Siddique, Onno Kampman, Yang Yang, Anik Dey and Pascale Fung</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-social">
        <div id="expander"></div><a href="#" class="session-title">Social Event (Vancouver Aquarium)</a><br/>        
        <span class="session-time">7:00 PM &ndash; 10:00 PM</span><br/>
        <span class="session-location btn btn--location">Vancouver Aquarium</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                
                <span class="info-button btn btn--small">Included in registration</span>

                <p>Enjoy a fun evening under the stars!</p>

                <p>Bring your Flower Power to our SoCal Beach Party! After the main dinner and Poster Session, join us on the Bayview Lawn adjacent to the Pavilion for desserts, coffee, tea, and drinks (cash bar). A Beach Boys style band will entertain you when you are not busy in the VW Bus Photo Booth, talking amongst your friends and colleagues, or playing with the beach balls.</p>

                <p>Learn more about the social event <a class="info-link" target="_blank" href="http://acl2017.org/participants/#social-event">here</a>.</p>
            </div>
        </div>
    </div>
    <div class="day" id="fourth-day">Wednesday, August 2</div>
    <div class="session session-plenary" id="session-breakfast-3">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
        <div class="session session-expandable session-plenary" id="session-invited-mirella">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk: Translating from Multiple Modalities to Text and Back</a><br/>
        <span class="session-people">Mirella Lapata (University of Edinburgh)</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:10 AM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grand Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Recent years have witnessed the development of a wide range of computational tools that process and generate natural language text. Many of these have become familiar to mainstream computer users in the from of web search, question answering, sentiment analysis, and notably machine translation. The accessibility of the web could be further enhanced with applications that not only translate between different languages (e.g., from English to French) but also within the same language, between different modalities, or different data formats. The web is rife with non-linguistic data (e.g., video, images, source code) that cannot be indexed or searched since most retrieval tools operate over textual data.</p>

                <p>In this talk I will argue that in order to render electronic data more accessible to individuals and computers alike, new types of translation models need to be developed.  I will focus on three examples, text simplification, source code generation, and movie summarization. I will illustrate how recent advances in deep learning can be extended in order to induce general representations for different modalities and learn how to translate between these and natural language.</p>
            </div>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-5">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:10 AM &ndash; 10:40 AM</span>
    </div>
        <div class="session session-expandable session-papers-outstanding1" id="session-7a">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 1</a><br/>
            <span class="session-time">10:40 AM &ndash; 12:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons A/B/C</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-7a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="151">
                        <td id="paper-time">10:40-10:58</td>
                        <td>
                            <span class="paper-title">Towards an Automatic Turing Test: Learning to Evaluate Dialogue Responses. </span><em>Ryan Lowe, Michael Noseworthy, Iulian Vlad Serban, Nicolas Angelard-Gontier, Yoshua Bengio and Joelle Pineau</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="152">
                        <td id="paper-time">10:59-11:17</td>
                        <td>
                            <span class="paper-title">A Transition-Based Directed Acyclic Graph Parser for UCCA. </span><em>Daniel Hershcovich, Omri Abend and Ari Rappoport</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="153">
                        <td id="paper-time">11:18-11:36</td>
                        <td>
                            <span class="paper-title">Abstract Syntax Networks for Code Generation and Semantic Parsing. </span><em>Maxim Rabinovich, Mitchell Stern and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="154">
                        <td id="paper-time">11:37-11:49</td>
                        <td>
                            <span class="paper-title">The Role of Prosody and Speech Register in Word Segmentation: A Computational Modelling Perspective. </span><em>Bogdan Ludusan, Reiko Mazuka, Mathieu Bernard, Alejandrina Cristia and Emmanuel Dupoux</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="155">
                        <td id="paper-time">11:50-12:02</td>
                        <td>
                            <span class="paper-title">A Two-stage Parsing Method for Text-level Discourse Analysis. </span><em>Yizhong Wang and Sujian Li</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="156">
                        <td id="paper-time">12:03-12:15</td>
                        <td>
                            <span class="paper-title">Error-repair Dependency Parsing for Ungrammatical Texts. </span><em>Keisuke Sakaguchi, Matt Post and Benjamin Van Durme</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers-outstanding2" id="session-7b">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 2</a><br/>
            <span class="session-time">10:40 AM &ndash; 12:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Salons D/E/F</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-7b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="157">
                        <td id="paper-time">10:40-10:58</td>
                        <td>
                            <span class="paper-title">Visualizing and Understanding Neural Machine Translation. </span><em>Yanzhuo Ding, Yang Liu, Huanbo Luan and Maosong Sun</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="158">
                        <td id="paper-time">10:59-11:17</td>
                        <td>
                            <span class="paper-title">Detecting annotation noise in automatically labelled data. </span><em>Ines Rehbein and Josef Ruppenhofer</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="159">
                        <td id="paper-time">11:18-11:30</td>
                        <td>
                            <span class="paper-title">Attention Strategies for Multi-Source Sequence-to-Sequence Learning. </span><em>Jindřich Libovický and Jindřich Helcl</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="160">
                        <td id="paper-time">11:31-11:43</td>
                        <td>
                            <span class="paper-title">Understanding and Detecting Diverse Supporting Arguments on Controversial Issues. </span><em>Xinyu Hua and Lu Wang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="161">
                        <td id="paper-time">11:44-11:56</td>
                        <td>
                            <span class="paper-title">A Neural Model for User Geolocation and Lexical Dialectology. </span><em>Afshin Rahimi, Trevor Cohn and Timothy Baldwin</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="162">
                        <td id="paper-time">11:57-12:09</td>
                        <td>
                            <span class="paper-title">A Corpus of Compositional Language for Visual Reasoning. </span><em>Alane Suhr, Mike Lewis, James Yeh and Yoav Artzi</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-plenary" id="session-lunch-3">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:15 PM &ndash; 1:30 PM</span>
    </div>
    <div class="session session-plenary" id="session-business-meeting">
        <a href="#" class="session-title">ACL Business Meeting</a><br/>
        <span class="session-people"><strong>All attendees are encouraged to participate in the business meeting.</strong></span><br/>
        <span class="session-time">1:00 PM &ndash; 2:30 PM</span><br/>
        <span class="session-location btn btn--location">Salons D/E/F</span>
    </div>
    <div class="session session-plenary" id="session-break-6">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">2:30 PM &ndash; 3:00 PM</span>
    </div>
    <div class="session session-expandable session-papers-outstanding1" id="session-8a">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 3</a><br/>
            <span class="session-time">3:00 PM &ndash; 4:40 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-8a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="163">
                        <td id="paper-time">3:00-3:18</td>
                        <td>
                            <span class="paper-title">Abstractive Document Summarization with a Graph-Based Attentional Neural Model. </span><em>Jiwei Tan and Xiaojun Wan</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="164">
                        <td id="paper-time">3:19-3:37</td>
                        <td>
                            <span class="paper-title">Probabilistic Typology: Deep Generative Models of Vowel Inventories. </span><em>Ryan Cotterell and Jason Eisner</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="165">
                        <td id="paper-time">3:38-3:56</td>
                        <td>
                            <span class="paper-title">Adversarial Multi-Criteria Learning for Chinese Word Segmentation. </span><em>Xinchi Chen, Zhan Shi, Xipeng Qiu and Xuanjing Huang</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="166">
                        <td id="paper-time">3:57-4:15</td>
                        <td>
                            <span class="paper-title">Neural Joint Model for Transition-based Chinese Syntactic Analysis. </span><em>Shuhei Kurita, Daisuke Kawahara and Sadao Kurohashi</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="167">
                        <td id="paper-time">4:16-4:34</td>
                        <td>
                            <span class="paper-title">Robust Incremental Neural Semantic Graph Parsing. </span><em>Jan Buys and Phil Blunsom</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>    
    <div class="session session-expandable session-papers-outstanding2" id="session-8b">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 4</a><br/>
            <span class="session-time">3:00 PM &ndash; 4:40 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-8b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper" paper-id="168">
                        <td id="paper-time">3:00-3:18</td>
                        <td>
                            <span class="paper-title">Joint Extraction of Entities and Relations Based on a Novel Tagging Scheme. </span><em>Suncong Zheng, Feng Wang and Hongyun Bao</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="169">
                        <td id="paper-time">3:19-3:37</td>
                        <td>
                            <span class="paper-title">A FOFE-based Local Detection Approach for Named Entity Recognition and Mention Detection. </span><em>Mingbin Xu, Hui Jiang and Sedtawut Watcharawittayakul</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="170">
                        <td id="paper-time">3:38-3:56</td>
                        <td>
                            <span class="paper-title">Vancouver Welcomes You! Minimalist Location Metonymy Resolution. </span><em>Milan Gritta, Mohammad Taher Pilehvar, Nut Limsopatham and Nigel Collier</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="171">
                        <td id="paper-time">3:57-4:15</td>
                        <td>
                            <span class="paper-title">Unifying Text, Metadata, and User Network Representations with a Neural Network for Geolocation Prediction. </span><em>Yasuhide Miura, Motoki Taniguchi, Tomoki Taniguchi and Tomoko Ohkuma</em>
                        </td>
                    </tr>
                    <tr id="paper" paper-id="172">
                        <td id="paper-time">4:16-4:34</td>
                        <td>
                            <span class="paper-title">Multi-Task Video Captioning with Visual and Textual Entailment. </span><em>Ramakanth Pasunuru and Mohit Bansal</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-plenary" id="session-lifetime-achievement">
        <span class="session-title">Lifetime Achivement Award</span><br/>        
        <span class="session-time">4:45 PM &ndash; 5:45 PM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grande Ballroom</span>
    </div>
    <div class="session session-plenary" id="session-closing-awards">
        <span class="session-title">Closing Session &amp; Awards</span><br/>        
        <span class="session-time">5:45 PM &ndash; 6:00 PM</span><br/>
        <span class="session-location btn btn--location">Bayshore Grande Ballroom</span>
    </div>
    <div id="generatePDFForm">
        <div id="formContainer">
            <input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
            <br/>
            <a href="#" id="generatePDFButton" class="btn btn--info btn--large">Generate PDF</a>
        </div>
    </div>
</div>
