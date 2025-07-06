import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { StartPage } from './pages/start/start';
import { Users } from './pages/users/users';
import { AuthGuard } from './services/auth.guard';
import { Devices } from './pages/devices/devices';
import { Data } from './pages/data/data';

export const routes: Routes = [
    { path: '', component: StartPage },
    { path: 'login', component: Login },
    { path: 'users', component: Users, canActivate: [AuthGuard] },
    { path: 'devices', component: Devices, canActivate: [AuthGuard] },
    { path: 'data', component: Data, canActivate: [AuthGuard] },
    { path: '**', redirectTo: '' } // Redirect to start page for any unknown routes
];
