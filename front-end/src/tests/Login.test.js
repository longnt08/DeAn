import { render, fireEvent, screen } from '@testing-library/react';
import Login from '../components/Login';

test('Login form submission', () => {
  const mockLogin = jest.fn();
  render(<Login login={mockLogin} />);

  fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'testuser' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
  fireEvent.click(screen.getByText('Login'));

  expect(mockLogin).toHaveBeenCalledWith('testuser', 'password');
});
