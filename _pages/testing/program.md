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

        function getPaperInfoFromTime(paperTimeObj) {

            /* get the paper session and day */
            var paperSession = paperTimeObj.parents('.session');
            var sessionDay = paperSession.prevAll('.day:first').text().trim();

            /* get the paper title */
            var paperTitle = paperTimeObj.siblings('td').text().trim();

            /* get the paper slot and the starting and ending times */
            var paperTimeText = paperTimeObj.text().trim();
            var paperTimes = paperTimeText.split('-');
            var paperSlotStart = paperTimes[0];
            var paperSlotEnd = paperTimes[1];
            var paperSlotAMPM = inferAMPM(paperSlotStart);
            var exactPaperStartingTime = sessionDay + ', 2017 ' + paperSlotStart + paperSlotAMPM;
            return [new Date(exactPaperStartingTime).toJSON(), paperSlotStart, paperSlotEnd, paperTitle, paperSession.attr('id')];
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
            return [new Date(exactTutorialStartingTime).toJSON(), tutorialSlotStart, tutorialSlotEnd, tutorialSession.attr('id')];
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
            return [new Date(exactPosterStartingTime).toJSON(), posterSlotStart, posterSlotEnd, posterSession.attr('id')];
        }

        function getConflicts(paperObject) {

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

        function populateHiddenProgramTable() {

            /* if no posters were selected from either or both of the two poster sessions, we still want a row showing the main plenary poster session information for the unchosen session(s) */
            var posterSessionKeys = Object.keys(chosenPostersHash);
            if (posterSessionKeys.length == 0) {
                var sessionNames = ['session-poster-1', 'session-poster-2'];
                for (var i=0; i<sessionNames.length; i++) {
                    var session = sessionInfoHash[sessionNames[i]];
                    var exactSessionStartingTime = session.day + ', 2017 ' + session.start;
                    var newPlenaryKey = new Date(exactSessionStartingTime).toJSON();
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
                var newPlenaryKey = new Date(exactSessionStartingTime).toJSON();
                if (!(newPlenaryKey in plenarySessionHash)) {
                    plenarySessionHash[newPlenaryKey] = unusedSession;
                }
            }

            /* concatenate the tutorial, poster and paper keys */
            var nonPlenaryKeys = Object.keys(chosenPapersHash).concat(Object.keys(chosenTutorialsHash)).concat(Object.keys(chosenPostersHash));

            /* if we are including plenary information in the PDF then sort its keys too and merge the two sets of keys together before sorting */
            var sortedPaperTimes = includePlenaryInSchedule ? nonPlenaryKeys.concat(Object.keys(plenarySessionHash)) : nonPlenaryKeys;
            sortedPaperTimes.sort(function(a, b) { return new Date(a) - new Date(b) });

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
                plenarySessionHash[new Date(exactSessionStartingTime).toJSON()] = session;
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

            $('body').on('click', 'div.session-expandable', function(event) {
                event.preventDefault();
                $(this).children('[class$="-details"]').slideToggle(300);
                $(this).children('#expander').toggleClass('expanded');
            });


            $('body').on('click', 'div.session-title', function(event) {
                event.preventDefault();
                $(this).children('[class$="-details"]').slideToggle(300);
                $(this).children('#expander').toggleClass('expanded');
            });

            /* when we mouse over a paper, highlight the conflicting papers */
            $('body').on('mouseover', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).addClass('hovered');
                $(conflictingPapers).addClass('hovered');
            });

            /* when we mouse out, remove all highlights */
            $('body').on('mouseout', 'table.paper-table tr#paper', function(event) {
                var conflictingPapers = getConflicts($(this));
                $(this).removeClass('hovered');
                $(conflictingPapers).removeClass('hovered');

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
                    var key = new Date(exactStartingTime).toJSON();
                    if (key in plenarySessionHash) {
                        delete plenarySessionHash[key];
                    }
                }
            });

            $('body').on('click', 'table.paper-table tr#paper', function(event, fromSession) {
                event.preventDefault();
                $(this).removeClass('hovered');
                getConflicts($(this)).removeClass('hovered');
                var paperTimeObj = $(this).children('td#paper-time');
                var paperInfo = getPaperInfoFromTime(paperTimeObj);
                var paperObject = {};
                var exactStartingTime = paperInfo[0];
                paperObject.start = paperInfo[1];
                paperObject.end = paperInfo[2];
                paperObject.title = paperInfo[3];
                paperObject.session = paperInfo[4];
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
                        <span class="tutorial-title">[T1] Natural Language Processing for Precision Medicine </span><br/><span class="btn btn--location inline-location">Executive 3AB</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T2] Multimodal Machine Learning </span><br/><span href="#" class="btn btn--location inline-location">Spinnaker</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T3] Deep Learning for Semantic Composition </span><br/><span href="#" class="btn btn--location inline-location">Marina 3</span>
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
        <span class="session-time">9:30 AM &ndash; 12:30 PM</span><br/>
        <div class="tutorial-session-details">
            <hr class="detail-separator"/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T4] Deep Learning for Dialogue Systems </span><br/><span class="btn btn--location inline-location">Executive 3AB</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T5] Beyond Words: Deep Learning for Multi-word Expressions and Collocations </span><br/><span href="#" class="btn btn--location inline-location">Spinnaker</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T6] Making Better Use of the Crowd</span><br/><span href="#" class="btn btn--location inline-location">Marina 3</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-reception">
        <span class="session-title">Welcome Reception</span><br/>     
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span><br/>
        <span class="session-location btn btn--location">Grande Foyer &amp; Terrace</span>
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
        <span class="session-location btn btn--location">Grande Ballroom</span>
    </div>
    <div class="session session-plenary" id="session-break-1">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:00 AM &ndash; 10:30 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-1a">
        <div id="expander"></div><a href="#" class="session-title">Information Extraction 1</a><br/>
            <span class="session-time">10:30 AM &ndash; 12:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Adversarial Multi-task Learning for Text Classification. </span><em>Pengfei Liu, Xipeng Qiu and Xuanjing Huang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Neural End-to-End Learning for Computational Argumentation Mining. </span><em>Steffen Eger, Johannes Daxenberger and Iryna Gurevych</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Neural Symbolic Machines: Learning Semantic Parsers on Freebase with Weak Supervision. </span><em>Chen Liang, Jonathan Berant, Quoc Le, Kenneth D. Forbus and Ni Lao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Neural Relation Extraction with Multi-lingual Attention. </span><em>Yankai Lin, Zhiyuan Liu and Maosong Sun</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Inducing Symbolic Meaning Representations for Semantic Parsing. </span><em>Jianpeng Cheng, Siva Reddy, Vijay Saraswat and Mirella Lapata</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Morph-fitting: Fine-Tuning Word Vector Spaces with Simple Language-Specific Rules. </span><em>Ivan Vulić, Nikola Mrkšić, Roi Reichart, Diarmuid Ó Séaghdha, Steve Young and Anna Korhonen</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Skip-Gram – Zipf + Uniform = Vector Additivity. </span><em>Alex Gittens, Dimitris Achlioptas and Michael W. Mahoney</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">The State of the Art in Semantic Representation. </span><em>Omri Abend and Ari Rappoport</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Joint Learning for Coreference Resolution. </span><em>Jing Lu and Vincent Ng</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Generating and Exploiting Large-scale Pseudo Training Data for Zero Pronoun Resolution. </span><em>Ting Liu, Yiming Cui, Qingyu Yin, Wei-Nan Zhang, Shijin Wang and Guoping Hu</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Discourse Mode Identification in Essays. </span><em>Wei Song</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Winning on the Merits: The Joint Effects of Content and Style on Debate Outcomes. </span><em>Lu Wang, Nick Beauchamp, Sarah Shugars, Kechen Qin</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">A Convolutional Encoder Model for Neural Machine Translation. </span><em>Jonas Gehring, Michael Auli, David Grangier and Yann Dauphin</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Deep Neural Machine Translation with Linear Associative Unit. </span><em>Mingxuan Wang, Zhengdong Lu, Jie Zhou and Qun Liu</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">A Polynomial-Time Dynamic Programming Algorithm for Phrase-Based Decoding with a Fixed Distortion Limit. </span><em>Yin-Wen Chang and Michael Collins</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Context Gates for Neural Machine Translation. </span><em>Zhaopeng Tu, Yang Liu, Zhengdong Lu, Xiaohua Liu, and Hang Li</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-1e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-1e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Neural AMR: Sequence-to-Sequence Models for Parsing and Generation. </span><em>Ioannis Konstas, Srinivasan Iyer, Mark Yatskar, Yejin Choi and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Program Induction for Rationale Generation: Learning to Solve and Explain Algebraic Word Problems. </span><em>Wang Ling, Dani Yogatama, Chris Dyer and Phil Blunsom</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Automatically Generating Rhythmic Verse with Neural Networks. </span><em>Jack Hopkins and Douwe Kiela</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Creating Training Corpora for Micro-Planners. </span><em>Claire Gardent, Anastasia Shimorina, Shashi Narayan and Laura Perez-Beltrachini</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Gated Self-Matching Networks for Reading Comprehension and Question Answering. </span><em>Wenhui Wang, Nan Yang, Furu Wei, Baobao Chang and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Generating Natural Answer by Incorporating Copying and Retrieving Mechanisms in Sequence-to-Sequence Learning. </span><em>Shizhu He, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Coarse-to-Fine Question Answering for Long Documents. </span><em>Eunsol Choi, Daniel Hewlett, Illia Polosukhin, Alexandre Lacoste, Jakob Uszkoreit and Jonathan Berant</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">An End-to-End Model for Question Answering over Knowledge Base with Cross-Attention Combining Global Knowledge. </span><em>Yanchao Hao, Yuanzhe Zhang, Shizhu He, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Translating Neuralese. </span><em>Jacob Andreas, Anca Dragan and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Combining distributional and referential information for naming objects through cross-modal mapping and direct word prediction. </span><em>Sina Zarrieß and David Schlangen</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">FOIL it! Find One mismatch between Image and Language caption. </span><em>Ravi Shekhar, Sandro Pezzelle, Yauhen Klimovich, Aurélie Herbelot, Moin Nabi, Enver Sangineto and Raffaella Bernardi</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Verb Physics: Relative Physical Knowledge of Actions and Objects. </span><em>Maxwell Forbes and Yejin Choi</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">A* CCG Parsing with a Supertag and Dependency Factored Model. </span><em>Masashi Yoshikawa, Hiroshi Noji and Yuji Matsumoto</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">A Full Non-Monotonic Transition System for Unrestricted Non-Projective Parsing. </span><em>Daniel Fernández-González and Carlos Gómez-Rodríguez</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Aggregating and Predicting Sequence Labels from Crowd Annotations. </span><em>An Thanh Nguyen, Byron Wallace, Junyi Jessy Li, Ani Nenkova and Matthew Lease</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Fine-Grained Prediction of Syntactic Typology: Discovering Latent Structure with Supervised Learning. </span><em>Dingquan Wang and Jason Eisner</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Multi-space Variational Encoder-Decoders for Semi-supervised Labeled Sequence Transduction. </span><em>Chunting Zhou and Graham Neubig</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Scalable Bayesian Learning of Recurrent Neural Networks for Language Modeling. </span><em>Zhe Gan, Chunyuan Li, Changyou Chen, Yunchen Pu, Qinliang Su and Lawrence Carin</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">Learning attention for historical text normalization by learning to pronounce. </span><em>Marcel Bollmann, Joachim Bingel and Anders Søgaard</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Deep Learning in Semantic Kernel Spaces. </span><em>Danilo Croce, Simone Filice, Giuseppe Castellucci and Roberto Basili</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-2e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-2e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:40-1:58</td>
                        <td>
                            <span class="paper-title">Handling Cold-Start Problem in Review Spam Detection by Jointly Embedding Texts and Behaviors. </span><em>Xuepeng Wang, Jun Zhao and Kang Liu</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:59-2:17</td>
                        <td>
                            <span class="paper-title">Learning Cognitive Features from Gaze Data for Sentiment and Sarcasm Classification using Convolutional Neural Network. </span><em>Abhijit Mishra, Kuntal Dey and Pushpak Bhattacharyya</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:18-2:36</td>
                        <td>
                            <span class="paper-title">An Unsupervised Neural Attention Model for Aspect Extraction. </span><em>Ruidan He, Wee Sun Lee, Hwee Tou Ng and Daniel Dahlmeier</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:37-2:55</td>
                        <td>
                            <span class="paper-title">Other Topics You May Also Agree or Disagree: Modeling Inter-Topic Preferences using Tweets and Matrix Factorization. </span><em>Akira Sasaki, Kazuaki Hanawa, Naoaki Okazaki and Kentaro Inui</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Automatically Labeled Data Generation for Large Scale Event Extraction. </span><em>Yubo Chen, Kang Liu and Jun Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Time Expression Analysis and Recognition Using Syntactic Token Types and General Heuristic Rules. </span><em>Xiaoshi Zhong, Aixin Sun and Erik Cambria</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Learning with Noise: Enhance Distantly Supervised Relation Extraction with Dynamic Transition Matrix. </span><em>Bingfeng Luo, Yansong Feng, Zheng Wang, Zhanxing Zhu, Songfang Huang, Rui Yan and Dongyan Zhao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Ordinal Common-sense Inference. </span><em>Sheng Zhang, Rachel Rudinger, Kevin Duh, Benjamin Van Durme</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">5:00-5:12</td>
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">A Syntactic Neural Model for General-Purpose Code Generation. </span><em>Pengcheng Yin and Graham Neubig</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Learning bilingual word embeddings with (almost) no bilingual data. </span><em>Mikel Artetxe, Gorka Labaka and Eneko Agirre</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Abstract Meaning Representation Parsing using LSTM Recurrent Neural Networks. </span><em>William Foland and James H. Martin</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Deep Semantic Role Labeling: What Works and What’s Next. </span><em>Luheng He, Kenton Lee, Mike Lewis and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">5:00-5:12</td>
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Towards End-to-End Reinforcement Learning of Dialogue Agents for Information Access. </span><em>Bhuwan Dhingra, Lihong Li, Xiujun Li, Jianfeng Gao, Yun-Nung Chen, Faisal Ahmed and Li Deng</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Sequential Matching Network: A New Architecture for Multi-turn Response Selection in Retrieval-based Chatbots. </span><em>Yu Wu, Wei Wu, Chen Xing, Ming Zhou and Zhoujun Li</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Learning Word-Like Units from Joint Audio-Visual Analysis. </span><em>David Harwath and James Glass</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Joint CTC-attention End-to-end Speech Recognition. </span><em>Shinji Watanabe, Takaaki Hori and John Hershey</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">5:00-5:12</td>
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">Found in Translation: Reconstructing Phylogenetic Language Trees from Translations. </span><em>Ella Rabinovich, Noam Ordan and Shuly Wintner</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">Predicting Native Language from Gaze. </span><em>Yevgeni Berzak, Chie Nakamura, Suzanne Flynn and Boris Katz</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Decoding Anagrammed Texts Written in an Unknown Language and Script. </span><em>Bradley Hauer and Grzegorz Kondrak</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Sparse Coding of Neural Word Embeddings for Multilingual Sequence Labeling. </span><em>Gábor Berend</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">5:00-5:12</td>
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-3e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-3e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:45-4:03</td>
                        <td>
                            <span class="paper-title">MORSE: Semantic-ally Drive-n MORpheme SEgment-er. </span><em>Tarek Sakakini, Suma Bhat and Pramod Viswanath</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:04-4:22</td>
                        <td>
                            <span class="paper-title">A Generative Model of Phonotactics. </span><em>Richard Futrell, Adam Albright, Peter Graff, and Timothy J. O’Donnell</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:23-4:41</td>
                        <td>
                            <span class="paper-title">Joint Semantic Synthesis and Morphological Analysis of the Derived Word. </span><em>Ryan Cotterell and Hinrich Schütze</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:42-5:00</td>
                        <td>
                            <span class="paper-title">Unsupervised Learning of Morphological Forests. </span><em>Jiaming Luo, Karthik, Narasimhan</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">5:00-5:12</td>
                        <td>
                            <span class="paper-title">Evaluation of Compound Splitting with Textual Entailment. </span><em>Glorianna Jagfeld, Patrick Ziering and Lonneke van der Plas</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>        
    <div class="session session-expandable session-posters" id="session-poster-1">
        <div id="expander"></div><a href="#" class="session-title">Posters &amp; Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 9:30 PM</span>
        <br/>
        <span class="session-location btn btn--location">Pavilion</span>
        <div class="poster-session-details">
            <hr class="detail-separator"/>
            <h4 style="text-decoration: underline;">Main Conference</h4>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Recurrent Neural Networks Approach for Estimating the Quality of Machine Translation Output. </span><em>Hyun Kim and Jong-Hyeok Lee</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Agreement on Target-bidirectional Neural Machine Translation. </span><em>Lemao Liu, Masao Utiyama, Andrew Finch and Eiichiro Sumita</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">An Unsupervised Model of Orthographic Variation for Historical Document Transcription. </span><em>Dan Garrette and Hannah Alpert-Abrams</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bidirectional RNN for Medical Event Detection in Electronic Health Records. </span><em>Abhyuday Jagannatha and Hong Yu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Breaking the Closed World Assumption in Text Classification. </span><em>Geli Fei and Bing Liu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Building Chinese Affective Resources in Valence-Arousal Dimensions. </span><em>Liang-Chih Yu, Lung-Hao Lee, Shuai Hao, Jin Wang, Yunchao He, Jun Hu, K. Robert Lai and Xuejie Zhang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Combining Recurrent and Convolutional Neural Networks for Relation Classification. </span><em>Ngoc Thang Vu, Heike Adel, Pankaj Gupta and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Conversational Markers of Constructive Discussions. </span><em>Vlad Niculae and Cristian Danescu-Niculescu-Mizil</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-lingual Wikification Using Multilingual Embeddings. </span><em>Chen-Tse Tsai and Dan Roth</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Deconstructing Complex Search Tasks: a Bayesian Nonparametric Approach for Extracting Sub-tasks. </span><em>Rishabh Mehrotra, Prasanta Bhattacharya and Emine Yilmaz</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Expectation-Regulated Neural Model for Event Mention Extraction. </span><em>Ching-Yun Chang, Zhiyang Teng and Yue Zhang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Grammatical error correction using neural machine translation. </span><em>Zheng Yuan and Ted Briscoe</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improved Neural Network-based Multi-label Classification with Better Initialization Leveraging Label Co-occurrence. </span><em>Gakuto Kurata, Bing Xiang and Bowen Zhou</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Improving event prediction by representing script participants. </span><em>Simon Ahrendt and Vera Demberg</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Individual Variation in the Choice of Referential Form. </span><em>Thiago Castro Ferreira, Emiel Krahmer and Sander Wubben</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Inferring Psycholinguistic Properties of Words. </span><em>Gustavo Paetzold and Lucia Specia</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Intra-Topic Variability Normalization based on Linear Projection for Topic Classification. </span><em>Quan Liu, Wu Guo, Zhen-Hua Ling, Hui Jiang and Yu Hu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Joint Learning Templates and Slots for Event Schema Induction. </span><em>Lei Sha, Sujian Li, Baobao Chang, Zhifang Sui and Zhifang Sui</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Large-scale Multitask Learning for Machine Translation Quality Estimation. </span><em>Kashif Shah and Lucia Specia</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Distributed Word Representations For Bidirectional LSTM Recurrent Neural Network. </span><em>Peilu Wang, Yao Qian, Frank Soong, Lei He and Hai Zhao</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Leverage Financial News to Predict Stock Price Movements Using Word Embeddings and Deep Neural Networks. </span><em>Yangtuo Peng and Hui Jiang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Multimodal Semantic Learning from Child-Directed Input. </span><em>Angeliki Lazaridou, Grzegorz Chrupała, Raquel Fernandez and Marco Baroni</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Online Multilingual Topic Models with Multi-Level Hyperpriors. </span><em>Kriste Krstovski, David Smith and Michael J. Kurtz</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Psycholinguistic Features for Deceptive Role Detection in Werewolf. </span><em>Codruta Girlea, Roxana Girju and Eyal Amir</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Recurrent Support Vector Machines For Slot Tagging In Spoken Language Understanding. </span><em>Yangyang Shi, Kaisheng Yao, Hu Chen, Dong Yu, Yi-Cheng Pan and Mei-Yuh Hwang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">STransE: a novel embedding model of entities and relationships in knowledge bases. </span><em>Dat Quoc Nguyen, Kairit Sirts, Lizhen Qu and Mark Johnson</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sequential Short-Text Classification with Recurrent and Convolutional Neural Networks. </span><em>Ji Young Lee and Franck Dernoncourt</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Shift-Reduce CCG Parsing using Neural Network Models. </span><em>Bharat Ram Ambati, Tejaswini Deoskar and Mark Steedman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Structured Prediction with Output Embeddings for Semantic Image Annotation. </span><em>Ariadna Quattoni, Arnau Ramisa, Pranava Swaroop Madhyastha, Edgar Simo-Serra and Francesc Moreno-Noguer</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Symmetric Patterns and Coordinations: Fast and Enhanced Representations of Verbs and Adjectives. </span><em>Roy Schwartz, Roi Reichart and Ari Rappoport</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">The Sensitivity of Topic Coherence Evaluation to Topic Cardinality. </span><em>Jey Han Lau and Timothy Baldwin</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Transition-Based Syntactic Linearization with Lookahead Features. </span><em>Ratish Puduppully, Yue Zhang and Manish Shrivastava</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Vision and Feature Norms: Improving automatic feature norm learning through cross-modal maps. </span><em>Luana Bulat, Douwe Kiela and Stephen Clark</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small poster-type">Student Research Workshop</span>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">An End-to-end Approach to Learning Semantic Frames with Feedforward Neural Network. </span><em>Yukun Feng, Yipei Xu and Dong Yu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Analogy-based detection of morphological and semantic relations with word embeddings: what works and what doesn't. </span><em>Anna Gladkova, Aleksandr Drozd and Satoshi Matsuoka</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Argument Identification in Chinese Editorials. </span><em>Marisa Chow</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatic tagging and retrieval of E-Commerce products based on visual features. </span><em>Vasu Sharma and Harish Karnick</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Combining syntactic patterns and Wikipedia's hierarchy of hyperlinks to extract relations: The case of meronymy extraction. </span><em>Debela Tesfaye Gemechu, Michael Zock and Solomon Teferra</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Data-driven Paraphrasing and Stylistic Harmonization. </span><em>Gerold Hintz</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Detecting 'Smart' Spammers on Social Network: A Topic Model Approach. </span><em>Linqing Liu, Yao Lu, Ye Luo, Renxian Zhang, Laurent Itti and Jianwei Lu</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Developing language technology tools and resources for a resource-poor language: Sindhi. </span><em>Raveesh Motlani</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small poster-type">System Demonstrations</span>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">rstWeb - A Browser-based Annotation Interface for Rhetorical Structure Theory and Discourse Relations. </span><em>Amir Zeldes</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Instant Feedback for Increasing the Presence of Solutions in Peer Reviews. </span><em>Huy Nguyen, Wenting Xiong and Diane Litman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Farasa: A Fast and Furious Segmenter for Arabic. </span><em>Ahmed Abdelali, Kareem Darwish, Nadir Durrani and Hamdy Mubarak</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">iAppraise: A Manual Machine Translation Evaluation Environment Supporting Eye-tracking. </span><em>Ahmed Abdelali, Nadir Durrani and Francisco Guzmán</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Linguistica 5: Unsupervised Learning of Linguistic Structure. </span><em>Jackson Lee and John Goldsmith</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">TransRead: Designing a Bilingual Reading Experience with Machine Translation Technologies. </span><em>François Yvon, Yong Xu, Marianna Apidianaki, Clément Pillias and Pierre Cubaud</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">New Dimensions in Testimony Demonstration. </span><em>Ron Artstein, Alesia Gainer, Kallirroi Georgila, Anton Leuski, Ari Shapiro and David Traum</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">ArgRewrite: A Web-based Revision Assistant for Argumentative Writings. </span><em>Fan Zhang, Rebecca Hwa, Diane Litman and Homa B. Hashemi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Scaling Up Word Clustering. </span><em>Jon Dehdari, Liling Tan and Josef van Genabith</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Task Completion Platform: A self-serve multi-domain goal oriented dialogue platform. </span><em>Paul Crook, Alex Marin, Vipul Agarwal, Khushboo Aggarwal, Tasos Anastasakos, Ravi Bikkula, Daniel Boies, Asli Celikyilmaz, Senthilkumar Chandramohan, Zhaleh Feizollahi, Roman Holenstein, Minwoo Jeong, Omar Khan, Young-Bum Kim, Elizabeth Krawczyk, Xiaohu Liu, Danko Panic, Vasiliy Radostev, Nikhil Ramesh, Jean-Phillipe Robichaud, Alexandre Rochette, Logan Stromberg and Ruhi Sarikaya</em>
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
    <div class="session session-expandable session-plenary" id="session-invited-speaker1">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk</a><br/>        
        <span class="session-people">Invited Speaker 1</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:10 AM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.</p>
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Deep Pyramid Convolutional Neural Networks for Text Categorization. </span><em>Rie Johnson and Tong Zhang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Improved Neural Relation Detection for Knowledge Base Question Answering. </span><em>Mo Yu, Wenpeng Yin, Kazi Saidul Hasan, Cicero dos Santos, Bing Xiang and Bowen Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Deep Keyphrase Generation. </span><em>Rui Meng, Daqing He, Sanqiang Zhao and Shuguang Han</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Attention-over-Attention Neural Networks for Reading Comprehension. </span><em>Yiming Cui, Zhipeng Chen, si wei, Shijin Wang, Ting Liu and Guoping Hu</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Alignment at Work: Using Language to Distinguish the Internalization and Self-Regulation Components of Cultural Fit in Organizations. </span><em>Gabriel Doyle, Amir Goldberg, Sameer Srivastava and Michael Frank</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Representations of language in a model of visually grounded speech signal. </span><em>Grzegorz Chrupała, Lieke Gelderloos and Afra Alishahi</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Spectral Analysis of Information Density in Dialogue Predicts Collaborative Task Performance. </span><em>Yang Xu and David Reitter</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Modeling Semantic Expectation: Using Script Knowledge for Referent Prediction. </span><em>Ashutosh Modi, Ivan Titov, Vera Demberg, Asad Sayeed, Manfred Pinkal</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Affect-LM: A Neural Language Model for Customizable Affective Text Generation. </span><em>Sayan Ghosh, Mathieu Chollet, Eugene Laksana, Stefan Scherer and Louis-Philippe Morency</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Domain Attention with an Ensemble of Experts. </span><em>Young-Bum Kim, Karl Stratos and Dongchan Kim</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Learning Discourse-level Diversity for Neural Dialog Models using Conditional Variational Autoencoders. </span><em>Tiancheng Zhao, Ran Zhao and Maxine Eskenazi</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Hybrid Code Networks: practical and efficient end-to-end dialog control with supervised and reinforcement learning. </span><em>Jason D Williams, Kavosh Asadi and Geoffrey Zweig</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Modeling Source Syntax for Neural Machine Translation. </span><em>Junhui Li, Deyi Xiong, Zhaopeng Tu, Muhua Zhu and Guodong Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">Sequence-to-Dependency Neural Machine Translation. </span><em>Shuangzhi Wu, Dongdong Zhang, Nan Yang, Mu Li and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Head-Lexicalized Bidirectional Tree LSTMs. </span><em>Zhiyang Teng and Yue Zhang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Pushing the Limits of Translation Quality Estimation. </span><em>André F. T. Martins, Marcin Junczys-Dowmunt, Fabio N. Kepler, Ramón Astudillo, Chris Hokamp, Roman Grundkiewicz</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-4e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-4e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:30-10:48</td>
                        <td>
                            <span class="paper-title">Detect Rumors in Microblog Posts Using Propagation Structure via Kernel Learning. </span><em>Ma Jing, Wei Gao and Kam-Fai Wong</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:49-11:07</td>
                        <td>
                            <span class="paper-title">EmoNet: Fine-Grained Emotion Detection with Gated Recurrent Neural Networks. </span><em>Muhammad Abdul-Mageed and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:08-11:26</td>
                        <td>
                            <span class="paper-title">Beyond Binary Labels: Political Ideology Prediction of Twitter Users. </span><em>Daniel Preoţiuc-Pietro, Ye Liu, Daniel Hopkins and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:27-11:45</td>
                        <td>
                            <span class="paper-title">Leveraging Behavioral and Social Information for Weakly Supervised Collective Classification of Political Discourse on Twitter. </span><em>Kristen Johnson and Dan Goldwasser</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:46-11:58</td>
                        <td>
                            <span class="paper-title">On the Distribution of Lexical Features in Social Media. </span><em>Fatemeh Almodaresi, Lyle Ungar, Vivek Kulkarni, Mohsen Zakeri, Salvatore Giorgi and H. Andrew Schwartz</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>    
    <div class="session session-plenary" id="session-lunch-arxiv">
        <span class="session-title">Bring your Own Lunch and Discuss: Double Blind Reviewing &amp; arXiv</span><br/>
        <span class="session-time">12:05 PM &ndash; 1:30 PM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-5a">
        <div id="expander"></div><a href="#" class="session-title">Multidisciplinary</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:30-1:42</td>
                        <td>
                            <span class="paper-title">Exploring Neural Text Simplification Models. </span><em>Sergiu Nisioi, Sanja Štajner, Simone Paolo Ponzetto and Liviu P. Dinu</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:43-2:01</td>
                        <td>
                            <span class="paper-title">A Nested Attention Neural Hybrid Model for Grammatical Error Correction. </span><em>Jianshu Ji, Qinlong Wang, Kristina Toutanova, Yongen Gong, Steven Truong and Jianfeng Gao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:02-2:20</td>
                        <td>
                            <span class="paper-title">TextFlow: A Text Similarity Measure based on Continuous Sequences. </span><em>Yassine Mrabet, Halil Kilicoglu and Dina Demner-Fushman</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:21-2:39</td>
                        <td>
                            <span class="paper-title">Friendships, Rivalries, and Trysts: Characterizing Relations between Ideas in Texts. </span><em>Chenhao Tan, Dallas Card and Noah A. Smith</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Polish evaluation dataset for compositional distributional semantics models. </span><em>Alina Wróblewska and Katarzyna Krasnowska-Kieraś</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">Automatic Annotation and Evaluation of Error Types for Grammatical Error Correction. </span><em>Christopher Bryant, Mariano Felice and Ted Briscoe</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Evaluation Metrics for Reading Comprehension: Prerequisite Skills and Readability. </span><em>Saku Sugawara, Yusuke Kido, Hikaru Yokono and Akiko Aizawa</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Sentence Alignment Methods for Improving Text Simplification Systems. </span><em>Sanja Štajner, Marc Franco-Salvador, Simone Paolo Ponzetto, Paolo Rosso and Heiner Stuckenschmidt</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">A Minimal Span-Based Neural Constituent Parser. </span><em>Mitchell Stern, Jacob Andreas and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">Semantic Dependency Parsing via Book Embedding. </span><em>Weiwei Sun, Junjie Cao and Xiaojun Wan</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Neural Word Segmentation with Rich Pretraining. </span><em>Jie Yang, Yue Zhang and Fei Dong</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Arc-swift: A Novel Transition System for Dependency Parsing. </span><em>Peng Qi and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Neural Machine Translation via Binary Code Prediction. </span><em>Yusuke Oda, Philip Arthur, Graham Neubig, Koichiro Yoshino and Satoshi Nakamura</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">What do Neural Machine Translation Models Learn about Morphology?. </span><em>Yonatan Belinkov, Nadir Durrani, Fahim Dalvi, Hassan Sajjad and James Glass</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:08-2:26</td>
                        <td>
                            <span class="paper-title">Fully Character-Level Neural Machine Translation without Explicit Segmentation. </span><em>Jason Lee, Kyunghyun Cho, Thomas Hofmann</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:27-2:39</td>
                        <td>
                            <span class="paper-title">Hybrid Neural Network Alignment and Lexicon Model in Direct HMM for Statistical Machine Translation. </span><em>Weiyue Wang, Derui Zhu and Hermann Ney</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:40-2:52</td>
                        <td>
                            <span class="paper-title">Towards String-To-Tree Neural Machine Translation. </span><em>Roee Aharoni and Yoav Goldberg</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers5" id="session-5e">
        <div id="expander"></div><a href="#" class="session-title">Sentiment 3</a><br/>
            <span class="session-time">1:30 PM &ndash; 3:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-5e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-5e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:30-1:48</td>
                        <td>
                            <span class="paper-title">Modeling Contextual Relationship Among Utterances in Multimodal Sentiment Analysis. </span><em>Soujanya Poria, Devamanyu Hazarika, Navonil Majumder and Erik Cambria</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">1:49-2:07</td>
                        <td>
                            <span class="paper-title">A Multidimensional Lexicon for Interpersonal Stancetaking. </span><em>Umashanthi Pavalanathan, Jim Fitzpatrick, Scott Kiesling and Jacob Eisenstein</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:08-2:20</td>
                        <td>
                            <span class="paper-title">Learning Lexical-Functional Patterns for First-Person Affect. </span><em>Lena Reed, Jiaqi Wu, Shereen Oraby, Pranav Anand and Marilyn Walker</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">2:21-2:33</td>
                        <td>
                            <span class="paper-title">Supervised Aspect Extraction with Knowledge Retention. </span><em>Lei Shu, Hu Xu and Bing Liu</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Tandem Anchoring: a Multiword Anchor Approach for Interactive Topic Modeling. </span><em>Jeffrey Lund, Connor Cook, Kevin Seppi and Jordan Boyd-Graber</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Comparing Apples to Apples: Learning Semantics of Common Entities Through a Novel Comprehension Task. </span><em>Omid Bakhshandeh and James Allen</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Going out on a limb : Joint Extraction of Entity Mentions and Relations without Dependency Trees. </span><em>Arzoo Katiyar and Claire Cardie</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Evaluating Visual Representations for Topic Understanding and Their Effects on Manually Generated Labels. </span><em>Alison Smith, Tak Yeon Lee, Forough-Poursabzi Sangdeh, Jordan Boyd-Graber, Niklas Elmqvist, Leah Findlater</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:41-4:53</td>
                        <td>
                            <span class="paper-title">Separating Reranking Effects from Model Combination Effects in Generative Neural Constituency Parsers. </span><em>Daniel Fried, Mitchell Stern and Dan Klein</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-papers2" id="session-6b">
        <div id="expander"></div><a href="#" class="session-title">Semantics 2</a><br/>
            <span class="session-time">3:25 PM &ndash; 5:00 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Naturalizing a Programming Language via Interactive Learning. </span><em>Sida I. Wang, Sam Ginn, Percy Liang and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Semantic Word Clusters Using Signed Spectral Clustering. </span><em>Joao Sedoc, Jean Gallier, Dean Foster and Lyle Ungar</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">An Interpretable Knowledge Transfer Model for Knowledge Base Completion. </span><em>Qizhe Xie, Xuezhe Ma, Zihang Dai and Eduard Hovy</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Learning a Neural Semantic Parser from User Feedback. </span><em>Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, Jayant Krishnamurthy and Luke Zettlemoyer</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6c-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Joint Modeling of Content and Discourse Relations in Dialogues. </span><em>Kechen Qin, Lu Wang, Joseph Kim and Julie Shah</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Argument Mining with Structured SVMs and RNNs. </span><em>Vlad Niculae, Claire Cardie and Joonsuk Park</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Neural Discourse Structure for Text Categorization. </span><em>Yangfeng Ji and Noah A. Smith</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Adversarial Connective-exploiting Networks for Implicit Discourse Relation Classification. </span><em>Lianhui Qin, Zhisong Zhang, Hai Zhao, Eric Xing and Zhiting Hu</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6d-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6d-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Bayesian Modeling of Lexical Resources for Low-Resource Settings. </span><em>Nicholas Andrews, Jason Eisner, Mark Dredze and Benjamin Van Durme</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Semi-Supervised QA with Generative Domain-Adaptive Nets. </span><em>Zhilin Yang, Junjie Hu, Ruslan Salakhutdinov and William Cohen</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">From Language to Programs: Bridging Reinforcement Learning and Maximum Marginal Likelihood. </span><em>Kelvin Guu, Panupong Pasupat, Evan Liu and Percy Liang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:22-4:34</td>
                        <td>
                            <span class="paper-title">Information-Theory Interpretation of the Skip-Gram Negative-Sampling Objective Function. </span><em>Oren Melamud and Jacob Goldberger</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-6e-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-6e-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:25-3:43</td>
                        <td>
                            <span class="paper-title">Diversity driven attention model for query-based abstractive summarization. </span><em>Preksha Nema, Mitesh M. Khapra, Balaraman Ravindran and Anirban Laha</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:44-4:02</td>
                        <td>
                            <span class="paper-title">Get To The Point: Summarization with Pointer-Generator Networks. </span><em>Abigail See, Peter J. Liu and Christopher D. Manning</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:03-4:21</td>
                        <td>
                            <span class="paper-title">Supervised Learning of Automatic Pyramid for Optimization-Based Multi-Document Summarization. </span><em>Maxime Peyrard and Judith Eckle-Kohler</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:22-4:40</td>
                        <td>
                            <span class="paper-title">Selective Encoding for Abstractive Sentence Summarization. </span><em>Qingyu Zhou, Nan Yang, Furu Wei and Ming Zhou</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
        <span class="session-time">5:40 PM &ndash; 7:40 PM</span><br/>
        <span class="session-location btn btn--location">Pavilion</span>
        <div class="poster-session-details">
            <hr class="detail-separator"/>
            <span class="info-button btn btn--small poster-type">Main Conference</span>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Assessing Relative Sentence Complexity using an Incremental CCG Parser. </span><em>Bharat Ram Ambati, Siva Reddy and Mark Steedman</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatic Prediction of Linguistic Decline in Writings of Subjects with Degenerative Dementia. </span><em>Davy Weissenbacher, Travis A. Johnson, Laura Wojtulewicz, Amylou Dueck, Dona Locke, Richard Caselli and Graciela Gonzalez</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Automatically Inferring Implicit Properties in Similes. </span><em>Ashequl Qadir, Ellen Riloff and Marilyn Walker</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">BIRA: Improved Predictive Exchange Word Clustering. </span><em>Jon Dehdari, Liling Tan and Josef van Genabith</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Bootstrapping Translation Detection and Sentence Extraction from Comparable Corpora. </span><em>Kriste Krstovski and David Smith</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Capturing Semantic Similarity for Entity Linking with Convolutional Neural Networks. </span><em>Matthew Francis-Landau, Greg Durrett and Dan Klein</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Consensus Maximization Fusion of Probabilistic Information Extractors. </span><em>Miguel Rodriguez, Sean Goldberg and Daisy Zhe Wang</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-genre Event Extraction with Knowledge Enrichment. </span><em>Hao Li and Heng Ji</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Deep Lexical Segmentation and Syntactic Parsing in the Easy-First Dependency Framework. </span><em>Matthieu Constant, Joseph Le Roux and Nadi Tomeh</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Discriminative Reranking for Grammatical Error Correction with Statistical Machine Translation. </span><em>Tomoya Mizumoto and Yuji Matsumoto</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Emergent: a novel data-set for stance classification. </span><em>William Ferreira and Andreas Vlachos</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Eyes Don't Lie: Predicting Machine Translation Quality Using Eye Movement. </span><em>Hassan Sajjad, Francisco Guzmán, Nadir Durrani, Ahmed Abdelali, Houda Bouamor, Irina Temnikova and Stephan Vogel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Fast and Easy Short Answer Grading with High Accuracy. </span><em>Md Arafat Sultan, Cristobal Salazar and Tamara Sumner</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Frustratingly Easy Cross-Lingual Transfer for Transition-Based Dependency Parsing. </span><em>Ophélie Lacroix, Lauriane Aufrant, Guillaume Wisniewski and François Yvon</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Geolocation for Twitter: Timing Matters. </span><em>Mark Dredze, Miles Osborne and Prabhanjan Kambadur</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Incorporating Side Information into Recurrent Neural Network Language Models. </span><em>Cong Duy Vu Hoang, Trevor Cohn and Gholamreza Haffari</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Integrating Morphological Desegmentation into Phrase-based Decoding. </span><em>Mohammad Salameh, Colin Cherry and Grzegorz Kondrak</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Interlocking Phrases in Phrase-based Statistical Machine Translation. </span><em>Ye Kyaw Thu, Andrew Finch and Eiichiro Sumita</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">K-Embeddings: Learning Conceptual Embeddings for Words using Context. </span><em>Thuy Vu and D. Stott Parker</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning Composition Models for Phrase Embeddings. </span><em>Mo Yu and Mark Dredze</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning a POS tagger for AAVE-like language. </span><em>Anna Jørgensen, Dirk Hovy and Anders Søgaard</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Learning to Recognize Ancillary Information for Automatic Paraphrase Identification. </span><em>Simone Filice and Alessandro Moschitti</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">MAWPS: A Math Word Problem Repository. </span><em>Rik Koncel-Kedziorski, Subhro Roy, Aida Amini, Nate Kushman and Hannaneh Hajishirzi</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Making Dependency Labeling Simple, Fast and Accurate. </span><em>Tianxiao Shen, Tao Lei and Regina Barzilay</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">PIC a Different Word: A Simple Model for Lexical Substitution in Context. </span><em>Stephen Roller and Katrin Erk</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">PRIMT: A Pick-Revise Framework for Interactive Machine Translation. </span><em>Shanbo Cheng, Shujian Huang, Huadong Chen, Xin-Yu Dai and Jiajun Chen</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Patterns of Wisdom: Discourse-Level Style in Multi-Sentence Quotations. </span><em>Kyle Booten and Marti A. Hearst</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Right-truncatable Neural Word Embeddings. </span><em>Jun Suzuki and Masaaki Nagata</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sentiment Composition of Words with Opposing Polarities. </span><em>Svetlana Kiritchenko and Saif Mohammad</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Simple, Fast Noise-Contrastive Estimation for Large RNN Vocabularies. </span><em>Barret Zoph, Ashish Vaswani, Jonathan May and Kevin Knight</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sparse Bilingual Word Representations for Cross-lingual Lexical Entailment. </span><em>Yogarshi Vyas and Marine Carpuat</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">The Instantiation Discourse Relation: A Corpus Analysis of Its Properties and Improved Detection. </span><em>Junyi Jessy Li and Ani Nenkova</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Visual Storytelling. </span><em>Ting-Hao Huang, Francis Ferraro, Nasrin Mostafazadeh, Ishan Misra, Jacob Devlin, Aishwarya Agrawal, Ross Girshick, Xiaodong He, Pushmeet Kohli, Dhruv Batra, Larry Zitnick, Devi Parikh, Lucy Vanderwende, Michel Galley and Margaret Mitchell</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small poster-type">Student Research Workshop</span>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Effects of Communicative Pressures on Novice L2 Learners' Use of Optional Formal Devices. </span><em>Yoav Binoun, Francesca Delogu, Clayton Greenberg, Mindaugas Mozuraitis and Matthew Crocker</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Explicit Argument Identification for Discourse Parsing In Hindi: A Hybrid Pipeline. </span><em>Rohit Jain and Dipti Sharma</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Exploring Fine-Grained Emotion Detection in Tweets. </span><em>Jasy Suet Yan Liew and Howard Turtle</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Extraction of Bilingual Technical Terms for Chinese-Japanese Patent Translation. </span><em>Wei Yang, Jinghui Yan and Yves Lepage</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Hateful Symbols or Hateful People? Predictive Features for Hate Speech Detection on Twitter. </span><em>Zeerak Waseem and Dirk Hovy</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Non-decreasing Sub-modular Function for Comprehensible Summarization. </span><em>Litton JKurisinkel, Pruthwik Mishra, Vigneshwaran Muralidaran, Vasudeva Varma and Dipti Misra Sharma</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Phylogenetic simulations over constraint-based grammar formalisms. </span><em>Andrew Lamont and Jonathan Washington</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Question Answering over Knowledge Base using Weakly Supervised Memory Networks. </span><em>Sarthak Jain</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Using Related Languages to Enhance Statistical Language Models. </span><em>Anna Currey, Alina Karakanta and Jon Dehdari</em>
                    </td>
                </tr>            
            </table>
            <span class="info-button btn btn--small poster-type">System Demonstrations</span>
            <table class="poster-table">
                <tr id="poster">
                    <td>
                        <span class="poster-title">Illinois Math Solver: Math Reasoning on the Web. </span><em>Subhro Roy and Dan Roth</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">LingoTurk: managing crowdsourced tasks for psycholinguistics. </span><em>Florian Pusse, Asad Sayeed and Vera Demberg</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Sentential Paraphrasing as Black-Box Machine Translation. </span><em>Courtney Napoles, Chris Callison-Burch and Matt Post</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">A Tag-based English Math Word Problem Solver with Understanding, Reasoning and Explanation. </span><em>Chao-Chun Liang, Kuang-Yi Hsu, Chien-Tsung Huang, Chung-Min Li, Shen-Yu Miao and Keh-Yih Su</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Cross-media Event Extraction and Recommendation. </span><em>Di Lu, Clare Voss, Fangbo Tao, Xiang Ren, Rachel Guan, Rostyslav Korolov, Tongtao Zhang, Dongang Wang, Hongzhi Li, Taylor Cassidy, Heng Ji, Shih-fu Chang, Jiawei Han, William Wallace, James Hendler, Mei Si and Lance Kaplan</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">SODA: Service Oriented Domain Adaptation Architecture for Microblog Categorization. </span><em>Himanshu Sharad Bhatt, Sandipan Dandapat, Peddamuthu Balaji, Shourya Roy, Sharmistha Jat and Deepali Semwal</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Lecture Translator - Speech translation framework for simultaneous lecture translation. </span><em>Markus Müller, Thai Son Nguyen, Jan Niehues, Eunah Cho, Bastian Krüger, Thanh-Le Ha, Kevin Kilgour, Matthias Sperber, Mohammed Mediani, Sebastian Stüker and Alex Waibel</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Zara The Supergirl: An Empathetic Personality Recognition System. </span><em>Pascale Fung, Anik Dey, Farhad Bin Siddique, Ruixi Lin, Yang Yang, Yan Wan and Ho Yin Ricky Chan</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">Kathaa: A Visual Programming Framework for NLP Applications. </span><em>Sharada Prasanna Mohanty, Nehal J Wani, Manish Srivastava and Dipti Misra Sharma</em>
                    </td>
                </tr>
                <tr id="poster">
                    <td>
                        <span class="poster-title">"Why Should I Trust You?": Explaining the Predictions of Any Classifier. </span><em>Marco Ribeiro, Sameer Singh and Carlos Guestrin</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-expandable session-plenary" id="session-social">
        <div id="expander"></div><a href="#" class="session-title">Social Event</a><br/>        
        <span class="session-time">7:00 PM &ndash; 10:00 PM</span><br/>
        <span class="session-location btn btn--location">Vancouver Aquarium</span>
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
    <div class="day" id="fourth-day">Wednesday, August 2</div>
    <div class="session session-plenary" id="session-breakfast-3">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
        <div class="session session-expandable session-plenary" id="session-invited-speaker2">
        <div id="expander"></div><a href="#" class="session-title">Invited Talk</a><br/>        
        <span class="session-people">Invited Speaker 2</span><br/>
        <span class="session-time">9:00 AM &ndash; 10:10 AM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <div class="session-abstract">
                <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.</p>
            </div>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-5">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:10 AM &ndash; 10:40 AM</span>
    </div>
        <div class="session session-expandable session-outstanding-papers1" id="session-7a">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 1</a><br/>
            <span class="session-time">10:40 AM &ndash; 12:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-7a-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:40-10:58</td>
                        <td>
                            <span class="paper-title">Towards an Automatic Turing Test: Learning to Evaluate Dialogue Responses. </span><em>Ryan Lowe, Michael Noseworthy, Iulian Vlad Serban, Nicolas Angelard-Gontier, Yoshua Bengio and Joelle Pineau</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:59-11:17</td>
                        <td>
                            <span class="paper-title">A Transition-Based Directed Acyclic Graph Parser for UCCA. </span><em>Daniel Hershcovich, Omri Abend and Ari Rappoport</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:18-11:36</td>
                        <td>
                            <span class="paper-title">Abstract Syntax Networks for Code Generation and Semantic Parsing. </span><em>Maxim Rabinovich, Mitchell Stern and Dan Klein</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:37-11:49</td>
                        <td>
                            <span class="paper-title">The Role of Prosody and Speech Register in Word Segmentation: A Computational Modelling Perspective. </span><em>Bogdan Ludusan, Reiko Mazuka, Mathieu Bernard, Alejandrina Cristia and Emmanuel Dupoux</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:50-12:02</td>
                        <td>
                            <span class="paper-title">A Two-stage Parsing Method for Text-level Discourse Analysis. </span><em>Yizhong Wang and Sujian Li</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">12:03-12:15</td>
                        <td>
                            <span class="paper-title">Error-repair Dependency Parsing for Ungrammatical Texts. </span><em>Keisuke Sakaguchi, Matt Post and Benjamin Van Durme</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>
    <div class="session session-expandable session-outstanding-papers2" id="session-7b">
        <div id="expander"></div><a href="#" class="session-title">Outstanding Papers 2</a><br/>
            <span class="session-time">10:40 AM &ndash; 12:15 PM</span>
            <br/>
            <span class="session-location btn btn--location">Grande Ballroom A</span>
            <div class="paper-session-details">
                <hr class="detail-separator"/>
                <a href="#" class="session-selector" id="session-7b-selector">
                Choose All</a>
                <a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a>
                <table class="paper-table">
                    <tr>
                        <td colspan="2">Chair: XXX</td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:40-10:58</td>
                        <td>
                            <span class="paper-title">Visualizing and Understanding Neural Machine Translation. </span><em>Yanzhuo Ding, Yang Liu, Huanbo Luan and Maosong Sun</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">10:59-11:17</td>
                        <td>
                            <span class="paper-title">Detecting annotation noise in automatically labelled data. </span><em>Ines Rehbein and Josef Ruppenhofer</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:18-11:30</td>
                        <td>
                            <span class="paper-title">Attention Strategies for Multi-Source Sequence-to-Sequence Learning. </span><em>Jindřich Libovický and Jindřich Helcl</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:31-11:43</td>
                        <td>
                            <span class="paper-title">Understanding and Detecting Diverse Supporting Arguments on Controversial Issues. </span><em>Xinyu Hua and Lu Wang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">11:44-11:56</td>
                        <td>
                            <span class="paper-title">A Neural Model for User Geolocation and Lexical Dialectology. </span><em>Afshin Rahimi, Trevor Cohn and Timothy Baldwin</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
        <span class="session-location btn btn--location">Grande Ballroom A</span>
    </div>
    <div class="session session-plenary" id="session-break-6">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">2:30 PM &ndash; 3:00 PM</span>
    </div>
    <div class="session session-expandable session-outstanding-papers1" id="session-8a">
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
                    <tr id="paper">
                        <td id="paper-time">3:00-3:18</td>
                        <td>
                            <span class="paper-title">Abstractive Document Summarization with a Graph-Based Attentional Neural Model. </span><em>Jiwei Tan and Xiaojun Wan</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:19-3:37</td>
                        <td>
                            <span class="paper-title">Probabilistic Typology: Deep Generative Models of Vowel Inventories. </span><em>Ryan Cotterell and Jason Eisner</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:38-3:56</td>
                        <td>
                            <span class="paper-title">Adversarial Multi-Criteria Learning for Chinese Word Segmentation. </span><em>Xinchi Chen, Zhan Shi, Xipeng Qiu and Xuanjing Huang</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:57-4:15</td>
                        <td>
                            <span class="paper-title">Neural Joint Model for Transition-based Chinese Syntactic Analysis. </span><em>Shuhei Kurita, Daisuke Kawahara and Sadao Kurohashi</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">4:16-4:34</td>
                        <td>
                            <span class="paper-title">Robust Incremental Neural Semantic Graph Parsing. </span><em>Jan Buys and Phil Blunsom</em>
                        </td>
                    </tr>
                </table>
            </div>
    </div>    
    <div class="session session-expandable session-outstanding-papers2" id="session-8b">
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
                    <tr id="paper">
                        <td id="paper-time">3:00-3:18</td>
                        <td>
                            <span class="paper-title">Joint Extraction of Entities and Relations Based on a Novel Tagging Scheme. </span><em>Suncong Zheng, Feng Wang and Hongyun Bao</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:19-3:37</td>
                        <td>
                            <span class="paper-title">A FOFE-based Local Detection Approach for Named Entity Recognition and Mention Detection. </span><em>Mingbin Xu, Hui Jiang and Sedtawut Watcharawittayakul</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:38-3:56</td>
                        <td>
                            <span class="paper-title">Vancouver Welcomes You! Minimalist Location Metonymy Resolution. </span><em>Milan Gritta, Mohammad Taher Pilehvar, Nut Limsopatham and Nigel Collier</em>
                        </td>
                    </tr>
                    <tr id="paper">
                        <td id="paper-time">3:57-4:15</td>
                        <td>
                            <span class="paper-title">Unifying Text, Metadata, and User Network Representations with a Neural Network for Geolocation Prediction. </span><em>Yasuhide Miura, Motoki Taniguchi, Tomoki Taniguchi and Tomoko Ohkuma</em>
                        </td>
                    </tr>
                    <tr id="paper">
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
        <span class="session-location btn btn--location">Grande Ballroom</span>
    </div>
    <div class="session session-plenary" id="session-lifetime-achievement">
        <span class="session-title">Closing Session &amp; Awards</span><br/>        
        <span class="session-time">5:45 PM &ndash; 6:00 PM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom</span>
    </div>
    <div id="generatePDFForm">
        <div id="formContainer">
            <input type="checkbox" id="includePlenaryCheckBox" value="second_checkbox"/>&nbsp;&nbsp;<span id="checkBoxLabel">Include plenary sessions in schedule</span>
            <br/>
            <a href="#" id="generatePDFButton" class="btn btn--info btn--large">Generate PDF</a>
        </div>
    </div>
</div>
