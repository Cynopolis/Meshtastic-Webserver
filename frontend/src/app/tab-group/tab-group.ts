import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';

/**
 * @title Basic use of the tab group
 */
@Component({
    selector: 'tab-group-test',
    templateUrl: 'tab-group.html',
    imports: [MatTabsModule],
})
export class TabGroup { }