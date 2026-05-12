import { useEffect, useState } from "react";

export default function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const es = new EventSource("/events/stream");
    es.onmessage = (e) => setEvents((prev) => [JSON.parse(e.data), ...prev]);
    return () => es.close();
  }, []);

  return (
    <main>
      <h1>DnD Live Events</h1>
      <ul>
        {events.map((ev, i) => (
          <li key={i}>{JSON.stringify(ev)}</li>
        ))}
      </ul>
    </main>
  );
}
