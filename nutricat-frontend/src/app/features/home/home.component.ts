import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CustomButtonComponent } from '../../shared/components/custom-button/custom-button.component';
import { Router } from "@angular/router";
import { AnimationOptions, LottieComponent } from 'ngx-lottie';
import { AnimationItem } from 'lottie-web';
import { AuthService } from '../../core/services/auth.service'; 

@Component({
  selector: 'app-home',
  imports: [CommonModule, CustomButtonComponent, LottieComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  private router = inject(Router);
  private authService = inject(AuthService);
  
  private animationItem: AnimationItem | undefined;

  options: AnimationOptions = {
    path: '/assets/animations/dance-cat.json',
    autoplay: false, 
    loop: true,
  };

  onEnterClick() {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/cats']);
    } else {
      this.router.navigate(['/auth']);
    }
  }
  
  animationCreated(animationItem: AnimationItem): void {
    this.animationItem = animationItem;
  }

  playAnimation(): void {
    this.animationItem?.play();
  }

  stopAnimation(): void {
    this.animationItem?.pause();
  }
}
