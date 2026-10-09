import api from '../../api';

// Values must match the `mood` enum in the database
const moods = [
  { value: 'good', label: 'Good', emoji: '😄' },
  { value: 'okay', label: 'Okay', emoji: '😐' },
  { value: 'bad', label: 'Bad', emoji: '😢' },
];

const MoodSelector = ({ mood, onMoodChange }) => {
  const handleMoodClick = async (value) => {
    const previous = mood;
    onMoodChange(value);
    try {
      await api.post("/mood/set", { mood: value });
    } catch (error) {
      console.error('Failed to update mood:', error);
      onMoodChange(previous);
    }
  };

  const selected = moods.find((m) => m.value === mood);

  return (
    <div className="bg-yellow-100 p-4 rounded-2xl shadow-md w-full max-w-xs text-center text-yellow-900">
      <h2 className="text-sm font-bold tracking-widest mb-3">HOW ARE YOU FEELING?</h2>
      <div className="flex justify-around items-center space-x-2">
        {moods.map(({ value, label, emoji }) => (
          <button
            key={value}
            onClick={() => handleMoodClick(value)}
            className={`text-3xl transition-transform transform hover:scale-125 ${
              mood === value ? 'ring-2 ring-yellow-500 rounded-full' : ''
            }`}
            title={label}
            aria-label={label}
            aria-pressed={mood === value}
          >
            {emoji}
          </button>
        ))}
      </div>
      {selected && (
        <p className="mt-2 text-sm text-yellow-800">You feel: <strong>{selected.label}</strong></p>
      )}
    </div>
  );
};

export default MoodSelector;
