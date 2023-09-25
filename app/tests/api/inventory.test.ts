import {
  DELETE as deleteInventory,
  GET as findInventory,
  PATCH as updateInventory,
} from "@/app/api/v0/city/[city]/inventory/[year]/route";
import { GET as calculateProgress } from "@/app/api/v0/city/[city]/inventory/[year]/progress/route";
import { POST as createInventory } from "@/app/api/v0/city/[city]/inventory/route";
import { db } from "@/models";
import { CreateInventoryRequest } from "@/util/validation";
import env from "@next/env";
import assert from "node:assert";
import { randomUUID } from "node:crypto";
import { after, before, beforeEach, describe, it } from "node:test";
import { Op } from "sequelize";
import { createRequest } from "../helpers";
import { SubSectorAttributes } from "@/models/SubSector";
import { City } from "@/models/City";

const locode = "XX_INVENTORY_CITY";

const inventory: CreateInventoryRequest = {
  inventoryName: "Test Inventory",
  year: 3000,
  totalEmissions: 1337,
};

const inventory2: CreateInventoryRequest = {
  inventoryName: "Test Inventory 2",
  year: 3001,
  totalEmissions: 1338,
};

const invalidInventory = {
  inventoryName: "",
  year: 0,
  totalEmissions: "246kg co2eq",
};

describe("Inventory API", () => {
  let city: City;
  before(async () => {
    const projectDir = process.cwd();
    env.loadEnvConfig(projectDir);
    await db.initialize();
    // this also deletes all Sector/SubSectorValue instances associated with it (cascade)
    await db.models.Inventory.destroy({
      where: { year: { [Op.or]: [inventory.year, inventory2.year] } },
    });
    await db.models.DataSource.destroy({
      where: { name: { [Op.like]: "XX_INVENTORY_TEST_%" } },
    });
    await db.models.City.destroy({ where: { locode } });
    city = await db.models.City.create({ cityId: randomUUID(), locode });
  });

  beforeEach(async () => {
    await db.models.Inventory.destroy({
      where: { cityId: city.cityId },
    });
    await db.models.Inventory.create({
      inventoryId: randomUUID(),
      cityId: city.cityId,
      ...inventory,
    });
  });

  after(async () => {
    if (db.sequelize) await db.sequelize.close();
  });

  it("should create an inventory", async () => {
    await db.models.Inventory.destroy({
      where: { year: inventory.year },
    });
    const url = "http://localhost:3000/api/v0/city" + locode;
    const req = createRequest(url, inventory);
    const res = await createInventory(req, {
      params: { city: locode },
    });
    assert.equal(res.status, 200);
    const { data } = await res.json();
    assert.equal(data.inventoryName, inventory.inventoryName);
    assert.equal(data.year, inventory.year);
    assert.equal(data.totalEmissions, inventory.totalEmissions);
  });

  it("should not create an inventory with invalid data", async () => {
    const url = "http://localhost:3000/api/v0/city/" + locode;
    const req = createRequest(url, invalidInventory);
    const res = await createInventory(req, {
      params: { city: locode },
    });
    assert.equal(res.status, 400);
    const {
      error: { issues },
    } = await res.json();
    assert.equal(issues.length, 3);
  });

  it("should find an inventory", async () => {
    const url = `http://localhost:3000/api/v0/city/${locode}/inventory/${inventory.year}`;
    const req = createRequest(url);
    const res = await findInventory(req, {
      params: { city: locode, year: inventory.year.toString() },
    });
    assert.equal(res.status, 200);
    const { data } = await res.json();
    assert.equal(data.inventoryName, inventory.inventoryName);
    assert.equal(data.year, inventory.year);
    assert.equal(data.totalEmissions, inventory.totalEmissions);
  });

  it("should not find non-existing inventories", async () => {
    const url = "http://localhost:3000/api/v0/city/XX_INVALID/inventory/0";
    const req = createRequest(url, invalidInventory);
    const res = await findInventory(req, {
      params: { city: "XX_INVALID", year: "0" },
    });
    assert.equal(res.status, 404);
  });

  it("should update an inventory", async () => {
    const url = `http://localhost:3000/api/v0/city/${locode}/inventory/${inventory.year}`;
    const req = createRequest(url, inventory2);
    const res = await updateInventory(req, {
      params: { city: locode, year: inventory.year.toString() },
    });
    assert.equal(res.status, 200);
    const { data } = await res.json();
    assert.equal(data.inventoryName, inventory2.inventoryName);
    assert.equal(data.year, inventory2.year);
    assert.equal(data.totalEmissions, inventory2.totalEmissions);
  });

  it("should not update an inventory with invalid data", async () => {
    const url = `http://localhost:3000/api/v0/city/${locode}/inventory/${inventory.year}`;
    const req = createRequest(url, invalidInventory);
    const res = await updateInventory(req, {
      params: { city: locode, year: inventory.year.toString() },
    });
    assert.equal(res.status, 400);
    const {
      error: { issues },
    } = await res.json();
    assert.equal(issues.length, 3);
  });

  it("should delete an inventory", async () => {
    const url = `http://localhost:3000/api/v0/city/${locode}/inventory/${inventory.year}`;
    const req = createRequest(url);
    const res = await deleteInventory(req, {
      params: { city: locode, year: inventory.year.toString() },
    });
    assert.equal(res.status, 200);
    const { data, deleted } = await res.json();
    assert.equal(deleted, true);
    assert.equal(data.inventoryName, inventory.inventoryName);
    assert.equal(data.year, inventory.year);
    assert.equal(data.totalEmissions, inventory.totalEmissions);
  });

  it("should not delete a non-existing inventory", async () => {
    const url = `http://localhost:3000/api/v0/city/XX_INVALID/inventory/0`;
    const req = createRequest(url);
    const res = await deleteInventory(req, {
      params: { city: "XX_INVALID", year: "0" },
    });
    assert.equal(res.status, 404);
  });

  it("should calculate progress for an inventory", async () => {
    // setup mock data
    const existingInventory = await db.models.Inventory.findOne({
      where: { year: inventory.year },
    });
    assert.notEqual(existingInventory, null);
    const sectorNames = ["TEST1", "TEST2", "TEST3"];
    const userSource = await db.models.DataSource.create({
      datasourceId: randomUUID(),
      sourceType: "user",
      name: "XX_INVENTORY_TEST_USER",
    });
    const thirdPartySource = await db.models.DataSource.create({
      datasourceId: randomUUID(),
      sourceType: "third_party",
      name: "XX_INVENTORY_TEST_THIRD_PARTY",
    });
    const sources = [userSource, thirdPartySource, null];

    for (const sectorName of sectorNames) {
      const sectorId = randomUUID();
      await db.models.Sector.create({
        sectorId,
        sectorName: "XX_INVENTORY_" + sectorName,
      });
      const sectorValueId = randomUUID();
      await db.models.SectorValue.create({
        sectorValueId,
        sectorId,
        inventoryId: existingInventory!.inventoryId,
      });
      for (let i = 0; i < sectorNames.length; i++) {
        const subsectorId = randomUUID();
        await db.models.SubSector.create({
          subsectorId,
          sectorId,
          subsectorName: "XX_INVENTORY_" + sectorName + "_" + sectorNames[i],
        });
        if (sources[i] != null) {
          await db.models.SubSectorValue.create({
            subsectorValueId: randomUUID(),
            subsectorId,
            sectorValueId,
            datasourceId: sources[i]?.datasourceId,
            inventoryId: existingInventory!.inventoryId,
          });
        }
      }
    }

    const url = `http://localhost:3000/api/v0/city/${locode}/inventory/${inventory.year}/progress`;
    const req = createRequest(url);
    const res = await calculateProgress(req, {
      params: { city: locode, year: inventory.year.toString() },
    });

    assert.equal(res.status, 200);
    const { totalProgress, sectorProgress } = (await res.json()).data;
    const cleanedSectorProgress = sectorProgress.map(
      ({
        sector,
        subSectors,
        ...progress
      }: {
        sector: { sectorName: string; sectorId: string; completed: boolean };
        subSectors: Array<SubSectorAttributes & { completed: boolean }>;
      }) => {
        assert.notEqual(sector.sectorId, null);
        assert.equal(subSectors.length, 3);
        for (const subSector of subSectors) {
          assert.notEqual(subSector.completed, null);
        }
        return { sector: { sectorName: sector.sectorName }, ...progress };
      },
    );
    assert.deepEqual(cleanedSectorProgress, [
      {
        total: 3,
        thirdParty: 1,
        uploaded: 1,
        sector: { sectorName: "XX_INVENTORY_TEST1" },
      },
      {
        total: 3,
        thirdParty: 1,
        uploaded: 1,
        sector: { sectorName: "XX_INVENTORY_TEST2" },
      },
      {
        total: 3,
        thirdParty: 1,
        uploaded: 1,
        sector: { sectorName: "XX_INVENTORY_TEST3" },
      },
    ]);
    assert.deepEqual(totalProgress, { total: 9, thirdParty: 3, uploaded: 3 });
  });
});