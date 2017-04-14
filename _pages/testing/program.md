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
                        <span class="tutorial-title">[T1] English Resource Semantics</span><br/><span class="btn btn--location inline-location">Executive 3AB</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T2] Multilingual Multimodal Language Processing Using Neural Networks</span><br/><span href="#" class="btn btn--location inline-location">Spinnaker</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T3] Question Answering with Knowledge Base, Web and Beyond</span><br/><span href="#" class="btn btn--location inline-location">Marina 3</span>
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
        <span class="session-time">2:00 PM &ndash; 5:00 PM</span>
        <div class="tutorial-session-details">
            <hr class="detail-separator"/>
            <table class="tutorial-table">
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T4] Recent Progress in Deep Learning for NLP</span><br/><span href="#" class="btn btn--location inline-location">Spinnaker</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T5] Scalable Statistical Relational Learning for NLP</span><br/><span href="#" class="btn btn--location inline-location">Marina 3</span>
                    </td>
                </tr>
                <tr id="tutorial">
                    <td>
                        <span class="tutorial-title">[T6] Statistical Machine Translation between Related Languages</span><br/><span href="#" class="btn btn--location inline-location">Executive 3AB</span>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-reception">
        <span class="session-title">Welcome Reception</span><br/>        
        <span class="session-time">6:00 PM &ndash; 9:00 PM</span>
        <span class="session-location btn btn--location">Grande Foyer &amp; Terrace</span>
    </div>
    <div class="day" id="second-day">Monday, July 31</div>
    <div class="session session-plenary" id="session-breakfast-1">
        <span class="session-title">Breakfast</span><br/>        
        <span class="session-time">7:30 AM &ndash; 8:45 AM</span>
    </div>
    <div class="session session-plenary" id="session-welcome">
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
    <div class="session session-plenary" id="session-break1">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:30 AM &ndash; 11:00 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-1a">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation I</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-1a-selector">
            Choose All</a>
            <a href="#" class="session-deselector" id="session-1a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: David Chiang</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">Achieving Accurate Conclusions in Evaluation of Automatic Machine Translation Metrics. </span><em>Yvette Graham and Qun Liu</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td><span class="paper-title">Flexible Non-Terminals for Dependency Tree-to-Tree Reordering. </span> <em>John Richardson, Fabien Cromieres, Toshiaki Nakazawa and Sadao Kurohashi</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td><span class="paper-title">Selecting Syntactic, Non-redundant Segments in Active Learning for Machine Translation. </span><em>Akiva Miura, Graham Neubig, Michael Paul and Satoshi Nakamura</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:10</td>
                    <td><span class="paper-title">Multi-Source Neural Translation. </span><em>Barret Zoph and Kevin Knight</em></td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:10-12:20</td>
                    <td><span class="paper-title">Controlling Politeness in Neural Machine Translation via Side Constraints. </span><em>Rico Sennrich, Barry Haddow and Alexandra Birch</em></td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
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
            <a href="#" class="session-selector" id="session-1b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-1b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Fei Liu</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">Neural Network-Based Abstract Generation for Opinions and Arguments. </span><em>Lu Wang and Wang Ling</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td>
                        <span class="paper-title">A Low-Rank Approximation Approach to Learning Joint Embeddings of News Stories and Images for Timeline Summarization. </span><em>William Yang Wang, Yashar Mehdad, Dragomir Radev and Amanda Stent</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td>
                        <span class="paper-title">Entity-balanced Gaussian pLSA for Automated Comparison. </span><em>Danish Contractor, Parag Singla and Mausam</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:10</td>
                    <td>
                        <span class="paper-title">Automatic Summarization of Student Course Feedback. </span><em>Wencan Luo, Fei Liu, Zitao Liu and Diane Litman</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:10-12:20</td>
                    <td>
                        <span class="paper-title">Abstractive Sentence Summarization with Attentive Recurrent Neural Networks. </span><em>Sumit Chopra, Michael Auli and Alexander M. Rush</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
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
            <a href="#" class="session-selector" id="session-1c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-1c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mari Ostendorf</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">Integer Linear Programming for Discourse Parsing. </span><em>Jérémy Perret, Stergos Afantenos, Nicholas Asher and Mathieu Morey</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td>
                        <span class="paper-title">A Diversity-Promoting Objective Function for Neural Conversation Models. </span><em>Jiwei Li, Michel Galley, Chris Brockett, Jianfeng Gao and Bill Dolan</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td>
                        <span class="paper-title">Multi-domain Neural Network Language Generation for Spoken Dialogue Systems. </span><em>Tsung-Hsien Wen, Milica Gasic, Nikola Mrkšić, Lina M. Rojas Barahona, Pei-Hao Su, David Vandyke and Steve Young</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:10</td>
                    <td>
                        <span class="paper-title">A Long Short-Term Memory Framework for Predicting Humor in Dialogues. </span><em>Dario Bertero and Pascale Fung</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:10-12:20</td>
                    <td>
                        <span class="paper-title">Conversational Flow in Oxford-style Debates. </span><em>Justine Zhang, Ravi Kumar, Sujith Ravi and Cristian Danescu-Niculescu-Mizil</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
                    <td>
                        <span class="paper-title">Counter-fitting Word Vectors to Linguistic Constraints. </span><em>Nikola Mrkšić, Diarmuid Ó Séaghdha, Blaise Thomson, Milica Gasic, Lina M. Rojas Barahona, Pei-Hao Su, David Vandyke, Tsung-Hsien Wen and Steve Young</em>
                    </td>
                </tr>
            </table>
        </div> 
    </div>
    <div class="session session-plenary" id="session-lunch-2">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 2:00 PM</span>
    </div>    
    <div class="session session-expandable session-papers1" id="session-2a">
        <div id="expander"></div><a href="#" class="session-title">Language and Vision</a><br/>        
        <span class="session-time">2:00 PM &ndash; 3:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-2a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-2a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Meg Mitchell</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:00-2:20</td>
                    <td>
                        <span class="paper-title">Grounded Semantic Role Labeling. </span><em>Shaohua Yang, Qiaozi Gao, Changsong Liu, Caiming Xiong, Song-Chun Zhu and Joyce Chai</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:20-2:40</td>
                    <td>
                        <span class="paper-title">Black Holes and White Rabbits: Metaphor Identification with Visual Features. </span><em>Ekaterina Shutova, Douwe Kiela and Jean Maillard</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:40-3:00</td>
                    <td>
                        <span class="paper-title">Bridge Correlational Neural Networks for Multilingual Multimodal Representation Learning. </span><em>Janarthanan Rajendran, Mitesh M Khapra, Sarath Chandar and Balaraman Ravindran</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:00-3:20</td>
                    <td>
                        <span class="paper-title">Unsupervised Visual Sense Disambiguation for Verbs using Multimodal Embeddings. </span><em>Spandana Gella, Mirella Lapata and Frank Keller</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:20-3:30</td>
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
            <a href="#" class="session-selector" id="session-2b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-2b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Alexander Rush</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:00-2:20</td>
                    <td>
                        <span class="paper-title">Efficient Structured Inference for Transition-Based Parsing with Neural Networks and Error States. </span><em>Ashish Vaswani and Kenji Sagae</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:20-2:40</td>
                    <td>
                        <span class="paper-title">Recurrent Neural Network Grammars. </span><em>Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros and Noah A. Smith</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:40-3:00</td>
                    <td>
                        <span class="paper-title">Expected F-Measure Training for Shift-Reduce Parsing with Recurrent Neural Networks. </span><em>Wenduan Xu, Michael Auli and Stephen Clark</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:00-3:20</td>
                    <td>
                        <span class="paper-title">LSTM CCG Parsing. </span><em>Mike Lewis, Kenton Lee and Luke Zettlemoyer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:20-3:30</td>
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
            <a href="#" class="session-selector" id="session-2c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-2c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Alessandro Moschitti</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:00-2:20</td>
                    <td>
                        <span class="paper-title">An Empirical Study of Automatic Chinese Word Segmentation for Spoken Language Understanding and Named Entity Recognition. </span><em>Wencan Luo and Fan Yang</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:20-2:40</td>
                    <td>
                        <span class="paper-title">Name Tagging for Low-resource Incident Languages based on Expectation-driven Learning. </span><em>Boliang Zhang, Xiaoman Pan, Tianlu Wang, Ashish Vaswani, Heng Ji, Kevin Knight and Daniel Marcu</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:40-3:00</td>
                    <td>
                        <span class="paper-title">Neural Architectures for Named Entity Recognition. </span><em>Guillaume Lample, Miguel Ballesteros, Kazuya Kawakami, Sandeep Subramanian and Chris Dyer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:00-3:20</td>
                    <td>
                        <span class="paper-title">Dynamic Feature Induction: The Last Gist to the State-of-the-Art. </span><em>Jinho D. Choi</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:20-3:30</td>
                    <td>
                        <span class="paper-title">Drop-out Conditional Random Fields for Twitter with Huge Mined Gazetteer. </span><em>Eun-Suk Yang, Young-Bum Kim, Ruhi Sarikaya and Yu-Seop Kim</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-2">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:30 PM &ndash; 4:00 PM</span>
    </div>   
    <div class="session session-expandable session-papers1" id="session-3a">
        <div id="expander"></div><a href="#" class="session-title">Event Detection</a><br/>        
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-3a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-3a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Heng Ji</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">Joint Extraction of Events and Entities within a Document Context. </span><em>Bishan Yang and Tom Mitchell</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">A Hierarchical Distance-dependent Bayesian Model for Event Coreference Resolution. </span><em>Bishan Yang, Claire Cardie and Peter Frazier</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-5:00</td>
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
            <a href="#" class="session-selector" id="session-3b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-3b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Chris Dyer</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">Top-down Tree Long Short-Term Memory Networks. </span><em>Xingxing Zhang, Liang Lu, Mirella Lapata</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">Recurrent Memory Networks for Language Modeling. </span><em>Ke Tran, Arianna Bisazza, Christof Monz</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-5:00</td>
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
            <a href="#" class="session-selector" id="session-3c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-3c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Marie-Catherine de Marneffe</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">Questioning Arbitrariness in Language: a Data-Driven Study of Conventional Iconicity. </span><em>Ekaterina Abramova and Raquel Fernandez</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">Distinguishing Literal and Non-Literal Usage of German Particle Verbs. </span><em>Maximilian Köper and Sabine Schulte im Walde</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-5:00</td>
                    <td>
                        <span class="paper-title">Phrasal Substitution of Idiomatic Expressions. </span><em>Changsheng Liu and Rebecca Hwa</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-3">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">5:00 PM &ndash; 5:15 PM</span>
    </div>  
    <div class="session session-expandable session-plenary" id="session-omm-1">
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
    <div class="session session-expandable session-posters" id="session-poster-1">
        <div id="expander"></div><a href="#" class="session-title">Posters, Demos &amp; Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
        <span class="session-location btn btn--location">Pavilion</span>
        <div class="poster-session-details">
            <hr class="detail-separator"/>
            <span class="info-button btn btn--small poster-type">Main Conference</span>
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
    <div class="session session-expandable session-papers1" id="session-4a">
        <div id="expander"></div><a href="#" class="session-title">Semantic Parsing</a><br/>
        <span class="session-time">9:00 AM &ndash; 10:30 AM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-4a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-4a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mike Lewis</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:00-9:20</td>
                    <td>
                        <span class="paper-title">Transforming Dependency Structures to Logical Forms for Semantic Parsing. </span><em>Siva Reddy, Oscar Täckström, Michael Collins, Tom Kwiatkowski, Dipanjan Das, Mark Steedman and Mirella Lapata</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:20-9:40</td>
                    <td>
                        <span class="paper-title">Imitation Learning of Agenda-based Semantic Parsers. </span><em>Jonathan Berant and Percy Liang</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:40-10:00</td>
                    <td>
                        <span class="paper-title">Probabilistic Models for Learning a Semantic Parser Lexicon. </span><em>Jayant Krishnamurthy</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:00-10:20</td>
                    <td>
                        <span class="paper-title">Semantic Parsing of Ambiguous Input through Paraphrasing and Verification. </span><em>Philip Arthur, Graham Neubig, Sakriani Sakti, Tomoki Toda and Satoshi Nakamura</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:20-10:30</td>
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
            <a href="#" class="session-selector" id="session-4b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-4b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Dilek Hakkani-Tur</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:00-9:20</td>
                    <td>
                        <span class="paper-title">Weighting Finite-State Transductions With Neural Context. </span><em>Pushpendre Rastogi, Ryan Cotterell and Jason Eisner</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:20-9:40</td>
                    <td>
                        <span class="paper-title">Morphological Inflection Generation Using Character Sequence to Sequence Learning. </span><em>Manaal Faruqui, Yulia Tsvetkov, Graham Neubig and Chris Dyer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:40-10:00</td>
                    <td>
                        <span class="paper-title">Towards Unsupervised and Language-independent Compound Splitting using Inflectional Morphological Transformations. </span><em>Patrick Ziering and Lonneke van der Plas</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:00-10:20</td>
                    <td>
                        <span class="paper-title">Phonological Pun-derstanding. </span><em>Aaron Jaech, Rik Koncel-Kedziorski and Mari Ostendorf</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:20-10:30</td>
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
            <a href="#" class="session-selector" id="session-4c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-4c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Jinho Choi</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:00-9:20</td>
                    <td>
                        <span class="paper-title">Syntactic Parsing of Web Queries with Question Intent. </span><em>Yuval Pinter, Roi Reichart and Idan Szpektor</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:20-9:40</td>
                    <td>
                        <span class="paper-title">Visualizing and Understanding Neural Models in NLP. </span><em>Jiwei Li, Xinlei Chen, Eduard Hovy and Dan Jurafsky</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">9:40-10:00</td>
                    <td>
                        <span class="paper-title">Bilingual Word Embeddings from Parallel and Non-parallel Corpora for Cross-Language Text Classification. </span><em>Aditya Mogadala and Achim Rettinger</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:00-10:20</td>
                    <td>
                        <span class="paper-title">Joint Learning with Global Inference for Comment Classification in Community Question Answering. </span><em>Shafiq Joty, Lluís Màrquez and Preslav Nakov</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:20-10:30</td>
                    <td>
                        <span class="paper-title">Weak Semi-Markov CRFs for Noun Phrase Chunking in Informal Text Aldrian. </span><em>Obaja Muis and Wei Lu</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-4">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:30 AM &ndash; 11:00 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-5a">
        <div id="expander"></div><a href="#" class="session-title">Generation</a><br/>
        <span class="session-time">11:00 AM &ndash; 12:30 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-5a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-5a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Lu Wang</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">What to talk about and how? Selective Generation using LSTMs with Coarse-to-Fine Alignment. </span><em>Hongyuan Mei, Mohit Bansal and Matthew Walter</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td>
                        <span class="paper-title">Generation from Abstract Meaning Representation using Tree Transducers. </span><em>Jeffrey Flanigan, Chris Dyer, Noah A. Smith and Jaime Carbonell</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td>
                        <span class="paper-title">A Corpus and Semantic Parser for Multilingual Natural Language Querying of OpenStreetMap. </span><em>Carolin Haas and Stefan Riezler</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:20</td>
                    <td>
                        <span class="paper-title">Natural Language Communication with Robots. </span><em>Yonatan Bisk, Daniel Marcu and Deniz Yuret</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
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
            <a href="#" class="session-selector" id="session-5b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-5b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ellen Riloff</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">Ultradense Word Embeddings by Orthogonal Transformation. </span><em>Sascha Rothe, Sebastian Ebert and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td>
                        <span class="paper-title">Separating Actor-View from Speaker-View Opinion Expressions using Linguistic Features. </span><em>Michael Wiegand, Marc Schulder and Josef Ruppenhofer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td>
                        <span class="paper-title">Clustering for Simultaneous Extraction of Aspects and Features from Reviews. </span><em>Lu Chen, Justin Martineau, Doreen Cheng and Amit Sheth</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:20</td>
                    <td>
                        <span class="paper-title">Opinion Holder and Target Extraction on Opinion Compounds -- A Linguistic Approach. </span><em>Michael Wiegand, Christine Bocionek and Josef Ruppenhofer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
                    <td>
                        <span class="paper-title">Capturing Reliable Fine-Grained Sentiment Associations by Crowdsourcing and Best-Worst Scaling. </span><em>Svetlana Kiritchenko and Saif Mohammad</em>
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
            <a href="#" class="session-selector" id="session-5c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-5c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ray Mooney</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:00-11:20</td>
                    <td>
                        <span class="paper-title">Concept Grounding to Multiple Knowledge Bases via Indirect Supervision. </span><em>Chen-Tse Tsai and Dan Roth</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:20-11:40</td>
                    <td>
                        <span class="paper-title">Mapping Verbs in Different Languages to Knowledge Base Relations using Web Text as Interlingua. </span><em>Derry Tanti Wijaya and Tom Mitchell</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:40-12:00</td>
                    <td>
                        <span class="paper-title">Comparing Convolutional Neural Networks to Traditional Models for Slot Filling. </span><em>Heike Adel, Benjamin Roth and Hinrich Schütze</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:00-12:20</td>
                    <td>
                        <span class="paper-title">A Corpus and Cloze Evaluation for Deeper Understanding of Commonsense Stories. </span><em>Nasrin Mostafazadeh, Nathanael Chambers, Xiaodong He, Devi Parikh, Dhruv Batra, Lucy Vanderwende, Pushmeet Kohli and James Allen</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:20-12:30</td>
                    <td>
                        <span class="paper-title">Dynamic Entity Representation with Max-pooling Improves Machine Reading. </span><em>Sosuke Kobayashi, Ran Tian, Naoaki Okazaki and Kentaro Inui</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-lunch-3">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:30 PM &ndash; 1:15 PM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-deep-learning-panel">
        <div id="expander"></div><a href="#" class="session-title">Panel Discussion: How Will Deep Learning Change Computational Linguistics?</a><br/>        
        <span class="session-time">1:15 PM &ndash; 2:15 PM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom</span>
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
                    <li>Is linguistics obsolete because DL will find better representations on its own? Or should DL be combined with traditional representations of latent linguistic structure? What is the best way to do that - hybrid architectures, hybrid training objectives, hand-designed input representations, or something else?</li>
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
            <a href="#" class="session-selector" id="session-6a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-6a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Colin Cherry</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:30-2:50</td>
                    <td>
                        <span class="paper-title">Speed-Constrained Tuning for Statistical Machine Translation Using Bayesian Optimization. </span><em>Daniel Beck, Adrià de Gispert, Gonzalo Iglesias, Aurelien Waite and Bill Byrne</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:50-3:10</td>
                    <td>
                        <span class="paper-title">Multi-Way, Multilingual Neural Machine Translation with a Shared Attention Mechanism. </span><em>Orhan Firat, Kyunghyun Cho and Yoshua Bengio</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:10-3:30</td>
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
            <a href="#" class="session-selector" id="session-6b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-6b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Byron Wallace</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:30-2:50</td>
                    <td>
                        <span class="paper-title">Multilingual Relation Extraction using Compositional Universal Schema. </span><em>Patrick Verga, David Belanger, Emma Strubell, Benjamin Roth and Andrew McCallum</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:50-3:10</td>
                    <td>
                        <span class="paper-title">Effective Crowd Annotation for Relation Extraction. </span><em>Angli Liu, Stephen Soderland, Jonathan Bragg, Christopher Lin, Xiao Ling and Daniel Weld</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:10-3:30</td>
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
            <a href="#" class="session-selector" id="session-6c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-6c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Dipanjan Das</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:30-2:50</td>
                    <td>
                        <span class="paper-title">DAG-Structured Long Short-Term Memory for Semantic Compositionality. </span><em>Xiaodan Zhu, Parinaz Sobhani and Hongyu Guo</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:50-3:10</td>
                    <td>
                        <span class="paper-title">Bayesian Supervised Domain Adaptation for Short Text Similarity. </span><em>Md Arafat Sultan, Jordan Boyd-Graber and Tamara Sumner</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:10-3:30</td>
                    <td>
                        <span class="paper-title">Pairwise Word Interaction Modeling with Deep Neural Networks for Semantic Similarity Measurement. </span><em>Hua He and Jimmy Lin</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-5">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">3:30 PM &ndash; 4:00 PM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-7a">
        <div id="expander"></div><a href="#" class="session-title">Machine Translation III</a><br/>
        <span class="session-time">4:00 PM &ndash; 5:00 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-7a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-7a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Marine Carpuat</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">An Attentional Model for Speech Translation Without Transcription. </span><em>Long Duong, Antonios Anastasopoulos, David Chiang, Steven Bird and Trevor Cohn</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">Information Density and Quality Estimation Features as Translationese Indicators for Human Translation Classification. </span><em>Raphael Rubino, Ekaterina Lapshinova-Koltunski and Josef van Genabith</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-4:50</td>
                    <td>
                        <span class="paper-title">Interpretese vs. Translationese: The Uniqueness of Human Strategies in Simultaneous Interpretation. </span><em>He He, Jordan Boyd-Graber and Hal Daumé III</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:50-5:00</td>
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
            <a href="#" class="session-selector" id="session-7b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-7b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Vincent Ng</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">A Novel Approach to Dropped Pronoun Translation. </span><em>Longyue Wang, Zhaopeng Tu, Xiaojun Zhang, Hang Li, Andy Way and Qun Liu</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">Learning Global Features for Coreference Resolution. </span><em>Sam Wiseman, Alexander M. Rush and Stuart Shieber</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-4:50</td>
                    <td>
                        <span class="paper-title">Search Space Pruning: A Simple Solution for Better Coreference Resolvers. </span><em>Nafise Sadat Moosavi and Michael Strube</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:50-5:00</td>
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
            <a href="#" class="session-selector" id="session-7c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-7c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Manaal Faruqui</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:00-4:20</td>
                    <td>
                        <span class="paper-title">Embedding Lexical Features via Low-Rank Tensors. </span><em>Mo Yu, Mark Dredze, Raman Arora and Matthew R. Gormley</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:20-4:40</td>
                    <td>
                        <span class="paper-title">The Role of Context Types and Dimensionality in Learning Word Embeddings. </span><em>Oren Melamud, David McClosky, Siddharth Patwardhan and Mohit Bansal</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">4:40-5:00</td>
                    <td>
                        <span class="paper-title">Improve Chinese Word Embeddings by Exploiting Internal Structure. </span><em>Jian Xu, Jiawei Liu, Liangang Zhang, Zhengyu Li and Huanhuan Chen</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-6">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">5:00 PM &ndash; 5:15 PM</span>
    </div>
    <div class="session session-expandable session-plenary" id="session-omm-2">
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
    <div class="session session-expandable session-posters" id="session-poster-2">
        <div id="expander"></div><a href="#" class="session-title">Posters, Demos &amp; Dinner</a><br/>        
        <span class="session-time">6:00 PM &ndash; 8:00 PM</span>
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
    <div class="day" id="fourth-day">Wednesday, August 2</div>
    <div class="session session-plenary" id="session-breakfast-3">
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
    <div class="session session-plenary" id="session-break-7">
        <span class="session-title">Break</span><br/>        
        <span class="session-time">10:15 AM &ndash; 10:45 AM</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-8a">
        <div id="expander"></div><a href="#" class="session-title">Question Answering</a><br/>
        <span class="session-time">10:45 AM &ndash; 12:15 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-8a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-8a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Ed Hovy</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:45-11:05</td>
                    <td>
                        <span class="paper-title">A Joint Model for Answer Sentence Ranking and Answer Extraction. </span><em>Md Arafat Sultan, Vittorio Castelli and Radu Florian</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:05-11:25</td>
                    <td>
                        <span class="paper-title">Convolutional Neural Networks vs. Convolution Kernels: Feature Engineering for Answer Sentence Reranking. </span><em>Kateryna Tymoshenko, Daniele Bonadiman and Alessandro Moschitti</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:25-11:45</td>
                    <td>
                        <span class="paper-title">Semi-supervised Question Retrieval with Gated Convolutions. </span><em>Tao Lei, Hrishikesh Joshi, Regina Barzilay, Tommi Jaakkola, Kateryna Tymoshenko, Alessandro Moschitti and Lluís Màrquez</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:45-12:05</td>
                    <td>
                        <span class="paper-title">Parsing Algebraic Word Problems into Equations. </span><em>Rik Koncel-Kedziorski, Hannaneh Hajishirzi, Ashish Sabharwal, Oren Etzioni and Siena Dumas Ang</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:05-12:15</td>
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
            <a href="#" class="session-selector" id="session-8b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-8b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Mohit Bansal</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:45-11:05</td>
                    <td>
                        <span class="paper-title">Multilingual Language Processing From Bytes. </span><em>Daniel Gillick, Cliff Brunk, Oriol Vinyals and Amarnag Subramanya</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:05-11:25</td>
                    <td>
                        <span class="paper-title">Ten Pairs to Tag -- Multilingual POS Tagging via Coarse Mapping between Embeddings. </span><em>Yuan Zhang, David Gaddy, Regina Barzilay and Tommi Jaakkola</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:25-11:45</td>
                    <td>
                        <span class="paper-title">Part-of-Speech Tagging for Historical English. </span><em>Yi Yang and Jacob Eisenstein</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:45-12:05</td>
                    <td>
                        <span class="paper-title">Statistical Modeling of Creole Genesis. </span><em>Yugo Murawaki</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:05-12:15</td>
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
            <a href="#" class="session-selector" id="session-8c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-8c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Hinrich Schütze</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">10:45-11:05</td>
                    <td>
                        <span class="paper-title">Bilingual Learning of Multi-sense Embeddings with Discrete Autoencoders. </span><em>Simon Suster, Ivan Titov and Gertjan van Noord</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:05-11:25</td>
                    <td>
                        <span class="paper-title">Polyglot Neural Language Models: A Case Study in Cross-Lingual Phonetic Representation Learning. </span><em>Yulia Tsvetkov, Sunayana Sitaram, Manaal Faruqui, Guillaume Lample, Patrick Littell, David R. Mortensen, Alan W Black, Lori Levin and Chris Dyer</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:25-11:45</td>
                    <td>
                        <span class="paper-title">Learning Distributed Representations of Sentences from Unlabelled Data. </span><em>Felix Hill, Kyunghyun Cho and Anna Korhonen</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">11:45-12:05</td>
                    <td>
                        <span class="paper-title">Learning to Understand Phrases by Embedding the Dictionary. </span><em>Felix Hill, Kyunghyun Cho, Anna Korhonen and Yoshua Bengio</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">12:05-12:15</td>
                    <td>
                        <span class="paper-title">Retrofitting Sense-Specific Word Vectors Using Parallel Text. </span><em>Allyson Ettinger, Philip Resnik and Marine Carpuat</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-lunch-4">
        <span class="session-title">Lunch</span><br/>        
        <span class="session-time">12:15 PM &ndash; 1:00 PM</span>
    </div>
    <div class="session session-plenary" id="session-business-meeting">
        <a href="#" class="session-title">NAACL Business Meeting</a><br/>
        <span class="session-people"><strong>All attendees are encouraged to participate in the business meeting.</strong></span><br/>
        <span class="session-time">1:00 PM &ndash; 2:00 PM</span><br/>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
    </div>
    <div class="session session-expandable session-papers1" id="session-9a">
        <div id="expander"></div><a href="#" class="session-title">Argumentation &amp; Discourse Relations</a><br/>
        <span class="session-time">2:15 PM &ndash; 3:45 PM</span>
        <span class="session-location btn btn--location">Grande Ballroom A</span>
        <div class="paper-session-details">
            <hr class="detail-separator"/>
            <a href="#" class="session-selector" id="session-9a-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-9a-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Cristian Danescu-Niculescu-Mizil</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:15-2:35</td>
                    <td>
                        <span class="paper-title">End-to-End Argumentation Mining in Student Essays. </span><em>Isaac Persing and Vincent Ng</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:35-2:55</td>
                    <td>
                        <span class="paper-title">Cross-Domain Mining of Argumentative Text through Distant Supervision. </span><em>Khalid Al Khatib, Henning Wachsmuth, Matthias Hagen, Jonas Köhler and Benno Stein</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:55-3:15</td>
                    <td>
                        <span class="paper-title">A Study of the Impact of Persuasive Argumentation in Political Debates. </span><em>Amparo Elizabeth Cano Basave and Yulan Hu</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:15-3:35</td>
                    <td>
                        <span class="paper-title">Lexical Coherence Graph Modeling Using Word Embeddings. </span><em>Mohsen Mesgar and Michael Strube</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:35-3:45</td>
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
            <a href="#" class="session-selector" id="session-9b-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-9b-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Steven Bethard</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:15-2:35</td>
                    <td>
                        <span class="paper-title">Automatic Generation and Scoring of Positive Interpretations from Negated Statements. </span><em>Eduardo Blanco and Zahra Sarabi</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:35-2:55</td>
                    <td>
                        <span class="paper-title">Learning Natural Language Inference with LSTM. </span><em>Shuohang Wang and Jing Jiang</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:55-3:15</td>
                    <td>
                        <span class="paper-title">Activity Modeling in Email. </span><em>Ashequl Qadir, Michael Gamon, Patrick Pantel and Ahmed Awadallah</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:15-3:35</td>
                    <td>
                        <span class="paper-title">Clustering Paraphrases by Word Sense. </span><em>Anne Cocos and Chris Callison-Burch</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:35-3:45</td>
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
            <a href="#" class="session-selector" id="session-9c-selector">Choose All</a>
            <a href="#" class="session-deselector" id="session-9c-deselector">Remove All</a>
            <table class="paper-table">
                <tr>
                    <td colspan="2">Chair: Jacob Eisenstein</td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:15-2:35</td>
                    <td>
                        <span class="paper-title">Hierarchical Attention Networks for Document Classification. </span><em>Zichao Yang, Diyi Yang, Chris Dyer, Xiaodong He, Alex Smola and Eduard Hovy</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:35-2:55</td>
                    <td>
                        <span class="paper-title">Dependency Based Embeddings for Sentence Classification Tasks. </span><em>Alexandros Komninos and Suresh Manandhar</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">2:55-3:15</td>
                    <td>
                        <span class="paper-title">Deep LSTM based Feature Mapping for Query Classification. </span><em>Yangyang Shi, Kaisheng Yao, Le Tian and Daxin Jiang</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:15-3:35</td>
                    <td>
                        <span class="paper-title">Dependency Sensitive Convolutional Neural Networks for Modeling Sentences and Documents. </span><em>Rui Zhang, Honglak Lee and Dragomir Radev</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">3:35-3:45</td>
                    <td>
                        <span class="paper-title">MGNC-CNN: A Simple Approach to Exploiting Multiple Word Embeddings for Sentence Classification. </span><em>Ye Zhang, Stephen Roller and Byron C. Wallace</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-break-8">
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
                <tr id="paper">
                    <td id="paper-time">4:15-4:35</td>
                    <td>
                    <span class="paper-title">Improving sentence compression by learning to predict gaze. </span><em>Sigrid Klerke, Yoav Goldberg and Anders Søgaard</em>
                    </td>
                </tr>
            </table>
            <span class="info-button btn btn--small">Best Long Papers</span>
            <table class="paper-table">
                <tr id="paper">
                    <td id="paper-time">4:35-5:05</td>
                    <td>
                        <span class="paper-title">Feuding Families and Former Friends; Unsupervised Learning for Dynamic Fictional Relationships. </span><em>Mohit Iyyer, Anupam Guha, Snigdha Chaturvedi, Jordan Boyd-Graber and Hal Daumé III</em>
                    </td>
                </tr>
                <tr id="paper">
                    <td id="paper-time">5:05-5:35</td>
                    <td>
                        <span class="paper-title">Learning to Compose Neural Networks for Question Answering. </span><em>Jacob Andreas, Marcus Rohrbach, Trevor Darrell and Dan Klein</em>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="session session-plenary" id="session-closing">
        <span class="session-title">Closing Remarks</span><br/>        
        <span class="session-time">5:35 PM &ndash; 5:45 PM</span>
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
