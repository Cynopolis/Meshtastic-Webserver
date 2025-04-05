import { importProvidersFrom } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { VERSION as MAT_VERSION, provideNativeDateAdapter } from '@angular/material/core';
import { TabGroup } from './app/tab-group/tab-group';

bootstrapApplication(TabGroup, {
  providers: [provideAnimations(), provideHttpClient(), provideNativeDateAdapter()],
}).catch(err => console.error(err));
