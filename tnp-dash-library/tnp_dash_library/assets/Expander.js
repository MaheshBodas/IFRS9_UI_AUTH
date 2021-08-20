window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        toggle_full_screen: function(n_clicks, id, btn_id) {

            if (n_clicks >=1) {
                try {
                    let $div_change = $(document.getElementById(id));
                    let $toggle = $(document.getElementById('toggle-button'));
                    let $i_change = $(document.getElementById(btn_id));
                    var $toolkit_labels = $(document.getElementsByClassName("toolkit-label"));
                    var $tabs = $(document.getElementsByClassName("tab-container--vert"));
                    var $charts = $(document.getElementsByClassName("expandable_chart-half"));
                    var $charts2 = $(document.getElementsByClassName("expandable_chart-full"));

                    if ($i_change.hasClass('glyphicon-resize-full')) {
                        $i_change.removeClass(' glyphicon-resize-full');
                        $i_change.addClass('glyphicon-resize-small');
                        $toggle.removeClass('btn_shown');
                        $toggle.addClass('hidden');

                        let i;
                        let j;
                        for (i = 0; i < $toolkit_labels.length; i++) {
                            $toolkit_labels[i].style.display = "None";
                        }
                        for (i = 0; i < $tabs.length; i++) {
                            $tabs[i].style.height = "30%";
                            let $span = $tabs[i].getElementsByTagName('span');

                            for (j = 0; j < $span.length; j++) {
                                $span[j].style.top = "10px";
                            }

                        }
                        for (i = 0; i < $charts.length; i++) {
                            $charts[i].style.height = "85vh";
                        }

                        for (i = 0; i < $charts2.length; i++) {
                            $charts2[i].style.height = "85vh";
                        }

                    } else if ($i_change.hasClass('glyphicon-resize-small')) {
                        $i_change.removeClass('glyphicon-resize-small');
                        $i_change.addClass('glyphicon-resize-full');
                        $toggle.removeClass('hidden');
                        $toggle.addClass('btn_shown');
                        let i;
                        let j;
                        for (i = 0; i < $toolkit_labels.length; i++) {
                            $toolkit_labels[i].style.display = "block";
                        }
                        for (i = 0; i < $tabs.length; i++) {
                            $tabs[i].style.height = "95.3%";
                            let $span = $tabs[i].getElementsByTagName('span');

                            for (j = 0; j < $span.length; j++) {
                                $span[j].style.top = "15px";
                            }
                        }
                        for (i = 0; i < $charts.length; i++) {
                            $charts[i].style.height = "31vh";
                        }
                        for (i = 0; i < $charts2.length; i++) {
                            $charts2[i].style.height = "72vh";
                        }
                    }

                    $div_change.closest('.panel').toggleClass('panel-fullscreen');

                    return "true";
                } catch (err) {
                    return "false";
                }
            }
        }
    }
});

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    sidepanel: {
        open_close_Nav: function(n_clicks, data) {

            if (n_clicks >=1) {

                let $div_change = $(document.getElementById("mySidepanel"));
                let $parent = $(document.getElementById('tabs-parent'));

                if (data == "Open") {
                    $div_change.addClass('sidepanel_closed');
                    $div_change.removeClass('sidepanel_open');
                    $parent.removeClass('squeeze-content');
                    return "Closed"
                } else {
                    $div_change.addClass('sidepanel_open');
                    $div_change.removeClass('sidepanel_closed');
                    $parent.addClass('squeeze-content');
                    return "Open"
                }
            }
        }
    }
});
