import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';
import { ApolloClient, InMemoryCache, createHttpLink, gql } from '@apollo/client/core';
import { setContext } from '@apollo/client/link/context';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-login',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  templateUrl: './login.html',
  styleUrl: './login.sass'
})
export class Login {
  loginForm: ReturnType<FormBuilder['group']>;
  loading = false;
  errorMessage = '';
  private apolloClient: ApolloClient<any>;

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });

    const httpLink = createHttpLink({ uri: environment.apiUrl });

    const authLink = setContext(() => {
      const token = localStorage.getItem('token');
      return {
        headers: {
          Authorization: token ? `Bearer ${token}` : '',
        },
      };
    });

    this.apolloClient = new ApolloClient({
      link: authLink.concat(httpLink),
      cache: new InMemoryCache(),
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;

    this.loading = true;
    this.errorMessage = '';

    const LOGIN_MUTATION = gql`
      mutation Login($email: String!, $password: String!) {
        loginUser(email: $email, password: $password) {
          token
        }
      }
    `;

    const { email, password } = this.loginForm.value;

    this.apolloClient
      .mutate({
        mutation: LOGIN_MUTATION,
        variables: { email, password },
      })
      .then((result: any) => {
        const token = result?.data?.loginUser?.token;
        if (token) {
          localStorage.setItem('token', token);
          this.router.navigate(['/']);
        } else {
          this.errorMessage = 'Login inválido';
        }
        this.loading = false;
      })
      .catch(() => {
        this.errorMessage = 'Credenciales incorrectas o error del servidor.';
        this.loading = false;
      });
  }
}
