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
function fibonacci(i)
    if (i <= 1)
        return 0
    if (i = 2)
        return 1
    previousNum1 <- 0
    previousNum2 <- 0
    currentNum <- 1
    while (i > 2)
        previousNum1 <- previousNum2
        previousNum2 <- currentNum
        currentNum <- previousNum1 + previousNum2
        i <- i - 1
    return currentNum

print(fibonacci(10))
          `.trim(),
        },
        {
            id: 'quicksort',
            name: 'Quick Sort',
            code: `
function exchange(A, i, j)
    temp <- A[i]
    A[i] <- A[j]
    A[j] <- temp

function Partition(A, p, r)
    x <- A[r]
    i <- p-1
    j <- p
    while (j < r)
        if (A[j] <= x)
            i <- i+1
            exchange(A, i, j)
        j <- j+1
    i <- i+1
    exchange(A, i, r)
    return i

function QuickSortInternal(A, p, r)
    if (p<r)
        q <- Partition(A, p, r)
        QuickSortInternal(A, p, q-1)
        QuickSortInternal(A, q+1, r)

function QuickSort(A)
    QuickSortInternal(A, 1, length(A))

Arr <- [0, 50, 86, 7, -24]
QuickSort(Arr)
print(Arr)
            `.trim(),
          },
          {
            id: 'binarySearch',
            name: 'Binary Search',
            code: `
    function binary_search_internal(A, l, r, x)
    if (l>r)
        return -1
    mid <- floor((l+r)/2)
    if (A[mid] = x)
        return mid
    if (A[mid] < x)
        return binary_search_internal(A, mid+1, r, x)
    return binary_search_internal(A, l, mid-1, x)

function binary_search(A, n, x)
    return binary_search_internal(A, 1, n, x)
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
