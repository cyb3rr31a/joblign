export default function HomePage() {
  return (
    <div className="bg-brand-background text-brand-text p-6 rounded shadow">
      <h1 className="text-2xl text-brand-primary">Welcome to Joblign</h1>
      <p className="text-brand-muted">Your next opportunity starts here.</p>
      <button className="mt-4 bg-brand-primary text-white px-4 py-2 rounded hover:bg-brand-secondary">
        Get Started
      </button>
    </div>
  )
  
}