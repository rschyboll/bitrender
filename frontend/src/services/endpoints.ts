export class ApiEndpoints {
  static Login = 'user/login';
  static Logged = 'user/logged';
  static Register = 'user/register';
  static Logout = 'user/logout';
  static UserMe = 'user/me';
  static Roles = 'roles';
  static RoleNew = 'roles/new';
  static RoleGetById = (id: string) => `roles/${id}`;
}
