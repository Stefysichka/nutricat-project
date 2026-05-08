import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CatService } from '../../../core/services/cat.service';

@Component({
  selector: 'app-cat',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './cat.component.html',
  styleUrl: './cat.component.scss'
})
export class CatComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router); 
  private catService = inject(CatService);

  cat: any = null;
  isLoading = true;

  showRationModal = false;
  isGeneratingRation = false;
  generatedRation = '';

  ngOnInit() {
    const catId = this.route.snapshot.paramMap.get('id');

    if (catId) {
      this.catService.getCatById(catId).subscribe({
        next: (data: any) => {
          this.cat = data;
          if (!this.cat.chart_data) {
            this.cat.chart_data = { protein: 0, fat: 0, fiber: 0 };
          }
          if (!this.cat.rations) {
            this.cat.rations = [];
          }
          if (!this.cat.photo_url) {
            this.cat.photo_url = ''; 
          }
          this.isLoading = false;
        },
        error: (err) => {
          console.error('Не вдалося завантажити котика:', err);
          this.isLoading = false;
        }
      });
    }
  }

  calculateAge(birthDateString: string): string {
    if (!birthDateString) return 'Невідомо';
    const birthDate = new Date(birthDateString);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear() - 1;
    const m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    return `${age} років`;
  }

  getNormalizedHeight(value: number): number {
    if (!this.cat || !this.cat.chart_data) return 0;
    const { protein, fat, fiber } = this.cat.chart_data;
    const max = Math.max(protein, fat, fiber, 1); 
    return (value / max) * 90; 
  }

  hasVetWarning(): boolean {
    if (!this.cat || !this.cat.tips) return false;
    return this.cat.tips.includes('[NEED_VET]');
  }

  get displayTips(): string {
    if (!this.cat || !this.cat.tips) return '';
    return this.cat.tips.replace('[NEED_VET]', '').trim();
  }

  findNearbyVets() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          const url = `https://www.google.com/maps/search/ветеринарна+клініка/@${lat},${lng},14z`;
          window.open(url, '_blank');
        },
        (error) => {
          console.warn('Локація недоступна або заборонена користувачем', error);
          window.open('https://www.google.com/maps/search/ветеринарна+клініка', '_blank');
        }
      );
    } else {
      window.open('https://www.google.com/maps/search/ветеринарна+клініка', '_blank');
    }
  }

  onPhotoSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: any) => {
        const base64Image = e.target.result;
        this.cat.photo_url = base64Image; 
        this.catService.updateCatPhoto(this.cat.id, base64Image).subscribe({
          next: () => console.log('Фото успішно збережено в базі!'),
          error: (err) => alert('Помилка при збереженні фото')
        });
      };
      reader.readAsDataURL(file);
    }
  }

  deleteProfile() {
    if (confirm(`Ви впевнені, що хочете видалити профіль котика ${this.cat.name}?`)) {
      this.catService.deleteCat(this.cat.id).subscribe({
        next: () => this.router.navigate(['/cats']),
        error: (err) => alert('Не вдалося видалити профіль.')
      });
    }
  }
  openRationModal() {
    this.showRationModal = true;
    this.isGeneratingRation = true;
    this.generatedRation = '';

    this.catService.generateIdealRation(this.cat.id).subscribe({
      next: (response: any) => {
        this.generatedRation = response.ration_text; 
        this.isGeneratingRation = false;
      },
      error: (err) => {
        console.error('Помилка ШІ:', err);
        this.generatedRation = 'Виникла помилка при генерації раціону. Спробуйте пізніше.';
        this.isGeneratingRation = false;
      }
    });
  }

  closeRationModal() {
    this.showRationModal = false;
  }
}