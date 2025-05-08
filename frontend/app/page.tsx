"use client"

import { useState } from "react"
import { PlusCircle, Truck, BarChart3 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { solveTransportation } from "@/lib/solver"

export default function TransportationSolver() {
  const [warehouses, setWarehouses] = useState<string[]>([])
  const [clients, setClients] = useState<string[]>([])
  const [warehouseInput, setWarehouseInput] = useState("")
  const [clientInput, setClientInput] = useState("")
  const [supply, setSupply] = useState<Record<string, number>>({})
  const [demand, setDemand] = useState<Record<string, number>>({})
  const [costMatrix, setCostMatrix] = useState<Record<string, number>>({})
  const [solution, setSolution] = useState<{
    objVal: number
    solution: Record<string, number>
  } | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const addWarehouse = () => {
    if (warehouseInput && !warehouses.includes(warehouseInput)) {
      setWarehouses([...warehouses, warehouseInput])
      setWarehouseInput("")
    }
  }

  const addClient = () => {
    if (clientInput && !clients.includes(clientInput)) {
      setClients([...clients, clientInput])
      setClientInput("")
    }
  }

  const updateSupply = (warehouse: string, value: number) => {
    setSupply({ ...supply, [warehouse]: value })
  }

  const updateDemand = (client: string, value: number) => {
    setDemand({ ...demand, [client]: value })
  }

  const updateCost = (warehouse: string, client: string, value: number) => {
    setCostMatrix({ ...costMatrix, [`${warehouse}_${client}`]: value })
  }

  const handleSolve = async () => {
    setLoading(true)
    setError(null)
    try {
      const formattedCostMatrix: Record<string, number> = {}
      for (const w of warehouses) {
        for (const c of clients) {
          formattedCostMatrix[`${w}_${c}`] = costMatrix[`${w}_${c}`] || 0
        }
      }

      const result = await solveTransportation(
        warehouses,
        clients,
        supply,
        demand,
        formattedCostMatrix
      )

      setSolution(result)
    } catch (error) {
      console.error("Error solving transportation problem:", error)
      setError(error instanceof Error ? error.message : 'An unknown error occurred')
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setWarehouses([])
    setClients([])
    setSupply({})
    setDemand({})
    setCostMatrix({})
    setSolution(null)
    setError(null)
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col items-center mb-8">
        <h1 className="text-3xl font-bold mb-2 flex items-center">
          <Truck className="mr-2" /> Transportation Problem Solver
        </h1>
        <p className="text-muted-foreground text-center max-w-2xl">
          Optimize the distribution of goods from warehouses to clients by minimizing transportation costs.
        </p>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {!solution ? (
        <div className="grid gap-8 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Warehouses (Supply)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                <Input
                  placeholder="Enter warehouse name"
                  value={warehouseInput}
                  onChange={(e) => setWarehouseInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && addWarehouse()}
                />
                <Button onClick={addWarehouse} size="icon">
                  <PlusCircle className="h-4 w-4" />
                </Button>
              </div>

              {warehouses.length > 0 && (
                <div className="space-y-4">
                  {warehouses.map((warehouse) => (
                    <div key={warehouse} className="flex gap-2 items-center">
                      <Label className="w-1/2">{warehouse}</Label>
                      <Input
                        type="number"
                        placeholder="Supply"
                        min="0"
                        onChange={(e) => updateSupply(warehouse, Number.parseInt(e.target.value))}
                      />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Clients (Demand)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                <Input
                  placeholder="Enter client name"
                  value={clientInput}
                  onChange={(e) => setClientInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && addClient()}
                />
                <Button onClick={addClient} size="icon">
                  <PlusCircle className="h-4 w-4" />
                </Button>
              </div>

              {clients.length > 0 && (
                <div className="space-y-4">
                  {clients.map((client) => (
                    <div key={client} className="flex gap-2 items-center">
                      <Label className="w-1/2">{client}</Label>
                      <Input
                        type="number"
                        placeholder="Demand"
                        min="0"
                        onChange={(e) => updateDemand(client, Number.parseInt(e.target.value))}
                      />
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {warehouses.length > 0 && clients.length > 0 && (
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Cost Matrix</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr>
                        <th className="p-2 border text-left">From / To</th>
                        {clients.map((client) => (
                          <th key={client} className="p-2 border text-left">
                            {client}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {warehouses.map((warehouse) => (
                        <tr key={warehouse}>
                          <td className="p-2 border font-medium">{warehouse}</td>
                          {clients.map((client) => (
                            <td key={`${warehouse}_${client}`} className="p-2 border">
                              <Input
                                type="number"
                                min="0"
                                placeholder="Cost"
                                onChange={(e) => updateCost(warehouse, client, Number.parseInt(e.target.value))}
                              />
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="mt-6 flex justify-center">
                  <Button
                    onClick={handleSolve}
                    disabled={loading || warehouses.length === 0 || clients.length === 0}
                    className="w-full md:w-auto"
                  >
                    {loading ? "Solving..." : "Solve Transportation Problem"}
                    {!loading && <BarChart3 className="ml-2 h-4 w-4" />}
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="mr-2" /> Optimal Transport Plan
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-4">
              <h3 className="text-xl font-bold mb-4">Total Cost: {solution.objVal.toFixed(2)}</h3>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="p-2 border text-left">From / To</th>
                    {clients.map((client) => (
                      <th key={client} className="p-2 border text-left">
                        {client}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {warehouses.map((warehouse) => (
                    <tr key={warehouse}>
                      <td className="p-2 border font-medium">{warehouse}</td>
                      {clients.map((client) => (
                        <td key={`${warehouse}_${client}`} className="p-2 border">
                          {solution.solution[`${warehouse}_${client}`]?.toFixed(2) || "0.00"}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-6 flex justify-center">
              <Button onClick={resetForm} variant="outline" className="w-full md:w-auto">
                Try Another Configuration
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}