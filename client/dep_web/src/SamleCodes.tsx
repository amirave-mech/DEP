import React from 'react';

interface SampleCodesProps {
  onSampleSelect: (code: string) => void;
}

const SampleCodes: React.FC<SampleCodesProps> = ({ onSampleSelect }) => {
  const sampleCodeOptions = [
    {
      id: 'fibonacci',
      name: 'Fibonacci Sequence',
      code: `
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a)
        a, b = b, a + b

fibonacci(10)
      `.trim(),
    },
    {
      id: 'hello_world',
      name: 'Hello World',
      code: `print("hello world!")`,
    },
    {
      id: 'factorial',
      name: 'Factorial Function',
      code: `
def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

print(factorial(5))
      `.trim(),
    },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = e.target.value;
    const selected = sampleCodeOptions.find(opt => opt.id === selectedId);
    if (selected) {
      onSampleSelect(selected.code);
    }
  };

  return (
    <select
      defaultValue=""
      onChange={handleChange}
      className="bg-transparent border border-gray-300 rounded px-2 py-1 text-sm cursor-pointer hover:border-gray-400 focus:outline-none"
    >
      <option value="" disabled>Select Sample Code</option>
      {sampleCodeOptions.map(option => (
        <option key={option.id} value={option.id} className="bg-white text-black">
          {option.name}
        </option>
      ))}
    </select>
  );
};

export default SampleCodes;
