import { Component } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { MatTableDataSource } from '@angular/material/table';
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core';
import { gql } from '@apollo/client/core';
import { setContext } from '@apollo/client/link/context';
import { environment } from '../../../environments/environment';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-users',
  imports: [CommonModule, MatTableModule, MatIconModule, MatProgressSpinnerModule],
  templateUrl: './users.html',
  styleUrl: './users.sass'
})
export class Users {
  dataSource = new MatTableDataSource<any>();
  displayedColumns: string[] = ['id', 'username', 'email', 'role'];
  loading = true;
  error = '';

  private apolloClient: ApolloClient<any>;

  constructor() {
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

    this.fetchUsers();
  }

  fetchUsers() {
    const USERS_QUERY = gql`
      query {
        users {
          id
          username
          email
          role
        }
      }
    `;

    this.apolloClient
      .query({ query: USERS_QUERY })
      .then((result: any) => {
        this.dataSource.data = result.data.users;
        this.loading = false;
      })
      .catch((err) => {
        console.error(err);
        this.error = 'Error al cargar usuarios.';
        this.loading = false;
      });
  }
}
