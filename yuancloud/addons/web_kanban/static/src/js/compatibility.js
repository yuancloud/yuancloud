yuancloud.define('web_kanban.compatibility', function (require) {
"use strict";

var kanban_widgets = require('web_kanban.widgets');
var KanbanRecord = require('web_kanban.Record');
var KanbanColumn = require('web_kanban.Column');
var KanbanView = require('web_kanban.KanbanView');

return;
yuancloud = window.yuancloud || {};
yuancloud.web_kanban = yuancloud.web_kanban || {};
yuancloud.web_kanban.AbstractField = kanban_widgets.AbstractField;
yuancloud.web_kanban.KanbanGroup = KanbanColumn;
yuancloud.web_kanban.KanbanRecord = KanbanRecord;
yuancloud.web_kanban.KanbanView = KanbanView;

});
