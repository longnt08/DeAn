import { render, fireEvent, screen } from '@testing-library/react';
import PaymentForm from '../components/PaymentForm';

test('Payment form submission', () => {
  const mockSubmitPayment = jest.fn();
  render(<PaymentForm token="fake-token" />);

  fireEvent.change(screen.getByPlaceholderText('Enter amount'), { target: { value: '100' } });
  fireEvent.click(screen.getByText('Submit Payment'));

  expect(mockSubmitPayment).toHaveBeenCalled();
});
