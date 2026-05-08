import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router'; 
import { CatService } from '../../../core/services/cat.service';
import { CustomButtonComponent } from '../../../shared/components/custom-button/custom-button.component';

@Component({
  selector: 'app-cat-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, CustomButtonComponent],
  templateUrl: './cat-chat.component.html',
  styleUrl: './cat-chat.component.scss'
})
export class CatChatComponent implements OnInit {
  private catService = inject(CatService);
  private router = inject(Router);
  private route = inject(ActivatedRoute); 

  messages: { role: string; content: string }[] = [];
  userInput: string = '';
  isLoading: boolean = false;
  isFinished: boolean = false;
  savedCatId: string = '';

  
  isEditMode: boolean = false;
  editCatId: string = '';

  ngOnInit() {
    
    this.route.queryParams.subscribe(params => {
      if (params['edit']) {
        this.isEditMode = true;
        this.editCatId = params['edit'];
        this.messages = [
          { role: 'assistant', content: `Привіт! Що змінилося в раціоні чи стані котика ${params['name']}?` }
        ];
      } else {
        this.messages = [
          { role: 'assistant', content: 'Привіт! Я ветеринарний асистент NutriCat. Розкажіть мені про вашого котика. Як його звати?' }
        ];
      }
    });
  }

  sendMessage() {
    if (!this.userInput.trim() || this.isLoading) return;

    this.messages.push({ role: 'user', content: this.userInput });
    this.userInput = '';
    this.isLoading = true;

    
    this.catService.sendChatMessage(this.messages, this.editCatId).subscribe({
      next: (response: any) => {
        this.isLoading = false;
        
        if (response.status === 'chatting') {
          this.messages.push(response.message);
        } else if (response.status === 'success') {
          this.isFinished = true;
          this.savedCatId = response.cat_id;
          
          let finalMsg = this.isEditMode 
            ? 'Дані успішно оновлено! Повертаємось до профілю.' 
            : 'Супер! Я зібрав усю інформацію. Переходимо на сторінку кота.';
            
          this.messages.push({ role: 'assistant', content: finalMsg });
        }
      },
      error: (err) => {
        this.isLoading = false;
        alert('Помилка з\'єднання з сервером.');
      }
    });
  }

  
  forceSave() {
    this.userInput = "Я закінчив вносити зміни. Будь ласка, проаналізуй все, напиши поради і збережи дані.";
    this.sendMessage();
  }

  goToProfile() {
    this.router.navigate(['/cats', this.savedCatId]);
  }
}