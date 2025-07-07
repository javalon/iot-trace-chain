import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';

@Component({
  selector: 'app-navbar',
  imports: [CommonModule, RouterModule, MatToolbarModule, MatButtonModule, MatMenuModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.sass'
})
export class Navbar {
  private auth: AuthService;

  constructor() {
    this.auth = inject(AuthService);
  }

  isAuthenticated(): boolean {
    return this.auth.isAuthenticated();
  }

  isAuthenticatedAndAdmin(): boolean {
    return this.auth.isAuthenticated() && this.auth.isAdmin();
  }

  getUserName(): string {
    const user = this.auth.getUserInfo();
    return user?.name || '';
  }

  logout(): void {
    this.auth.clearToken();
    location.reload(); // o redirigir a login
  }
}
