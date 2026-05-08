import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideLottieOptions } from 'ngx-lottie';
import player from 'lottie-web';
import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './core/interceptors/auth.interceptor'; 

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideLottieOptions({
    player: () => player,
  }), provideHttpClient(), provideHttpClient(withInterceptors([authInterceptor]))]
};
