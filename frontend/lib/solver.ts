import { toast } from 'react-hot-toast';

export async function solveTransportation(
  warehouses: string[],
  clients: string[],
  supply: Record<string, number>,
  demand: Record<string, number>,
  costMatrix: Record<string, number>,
) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        warehouses,
        clients,
        supply,
        demand,
        costMatrix,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      toast.error(data.error || 'No solution found for transportation problem');
      throw new Error(data.error || 'Failed to solve transportation problem');
    }

    return data;

  } catch (error) {
    console.error('Error calling solver API:', error);
    throw error;
  }
}