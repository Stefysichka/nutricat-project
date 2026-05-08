import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CatService } from '../../core/services/cat.service';
import { CustomButtonComponent } from '../../shared/components/custom-button/custom-button.component';

@Component({
  selector: 'app-cats',
  standalone: true,
  imports: [CommonModule, RouterLink, CustomButtonComponent],
  templateUrl: './cats.component.html',
  styleUrl: './cats.component.scss'
})
export class CatsComponent implements OnInit {
  private catService = inject(CatService);

  cats: any[] = [];
  isLoading = true;

  ngOnInit() {
    this.catService.getCats().subscribe({
      next: (data: any) => {
        this.cats = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Помилка завантаження котів', err);
        this.isLoading = false;
      }
    });
  }
  calculateAge(birthDateString: string): string {
    if (!birthDateString) return 'Невідомо';
    const birthDate = new Date(birthDateString);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear() -1;
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return `${age} років`;
  }
}