"use client";
import { useState, useEffect } from "react";
import { supabase } from "../../lib/supabase";

export default function Dashboard() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [catalogText, setCatalogText]     = useState("");
  const [shopId]                          = useState("fatima_01");
  const [status, setStatus]               = useState("");

  useEffect(() => { loadConversations(); }, []);

  async function loadConversations() {
    const { data } = await supabase
      .from("conversations")
      .select("*")
      .eq("shop_id", shopId)
      .order("created_at", { ascending: false })
      .limit(20);
    setConversations(data || []);
  }

  async function uploadCatalog() {
    setStatus("Uploading...");
    const lines = catalogText.split("\n").filter(l => l.trim() !== "");
    const items = lines.map((line, i) => ({ id: String(i + 1), text: line.trim() }));
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/catalog`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ shop_id: shopId, items })
    });
    const data = await res.json();
    setStatus(`✅ ${data.items_added} items uploaded!`);
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-green-400">وكيل — Wekil</h1>
        <p className="text-gray-400">Dashboard for {shopId}</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* Catalog Upload */}
        <div className="bg-gray-900 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">📦 Upload Catalog</h2>
          <p className="text-gray-400 text-sm mb-3">
            One product per line.<br/>
            مثال: جيلابة حمراء - 350 درهم، مقاسات S/M/L
          </p>
          <textarea
            className="w-full bg-gray-800 rounded-lg p-3 text-sm h-48 resize-none focus:outline-none focus:ring-2 focus:ring-green-400"
            placeholder="اكتب المنتجات هنا..."
            value={catalogText}
            onChange={e => setCatalogText(e.target.value)}
          />
          <button
            onClick={uploadCatalog}
            className="mt-3 w-full bg-green-500 hover:bg-green-400 text-black font-bold py-2 rounded-lg transition"
          >
            Upload
          </button>
          {status && <p className="mt-2 text-sm text-green-400">{status}</p>}
        </div>

        {/* Conversations */}
        <div className="bg-gray-900 rounded-xl p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">💬 Conversations</h2>
            <button onClick={loadConversations} className="text-sm text-green-400 hover:underline">
              Refresh
            </button>
          </div>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {conversations.length === 0 && (
              <p className="text-gray-500 text-sm">No conversations yet.</p>
            )}
            {conversations.map(msg => (
              <div key={msg.id} className={`p-3 rounded-lg text-sm text-right ${
                msg.role === "user" ? "bg-gray-800" : "bg-green-900"
              }`}>
                <span className="text-xs text-gray-400 block mb-1">
                  {msg.role === "user" ? "👤 زبون" : "🤖 Wekil"} — {msg.customer_phone}
                </span>
                {msg.content}
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}