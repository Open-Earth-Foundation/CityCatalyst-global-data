import * as Sequelize from "sequelize";
import { DataTypes, Model, Optional } from "sequelize";
import { User, UserId } from "./User";

export interface UserFileAttributes {
  id: string;
  userId?: string;
  fileReference?: string;
  data?: Buffer | any;
  fileType?: string;
  fileName?: string;
  sector?: string;
  status?: string;
  url?: string;
  gpcRefNo?: string;
  created?: Date;
  lastUpdated?: Date;
}

export type UserFilePk = "id";
export type UserFileId = UserFile[UserFilePk];
export type UserFileOptionalAttributes =
  | "userId"
  | "fileReference"
  | "data"
  | "fileType"
  | "fileName"
  | "sector"
  | "url"
  | "status"
  | "gpcRefNo"
  | "created"
  | "lastUpdated";
export type UserFileCreationAttributes = Optional<
  UserFileAttributes,
  UserFileOptionalAttributes
>;

export class UserFile
  extends Model<UserFileAttributes, UserFileCreationAttributes>
  implements UserFileAttributes
{
  id!: string;
  userId?: string | undefined;
  fileReference?: string | undefined;
  data: Buffer | undefined;
  fileType?: string | undefined;
  fileName?: string | undefined;
  sector?: string | undefined;
  url?: string | undefined;
  status: string | undefined;
  gpcRefNo?: string | undefined;
  created?: Date | undefined;
  lastUpdated?: Date | undefined;

  //UserFile belongs to User via id
  user!: User;
  getUser!: Sequelize.BelongsToGetAssociationMixin<User>;
  setUser!: Sequelize.BelongsToSetAssociationMixin<User, UserId>;
  createUser!: Sequelize.BelongsToCreateAssociationMixin<User>;

  static initModel(sequelize: Sequelize.Sequelize): typeof UserFile {
    return UserFile.init(
      {
        id: {
          type: DataTypes.UUID,
          allowNull: false,
          primaryKey: true,
          field: "id",
        },
        userId: {
          type: DataTypes.UUID,
          allowNull: true,
          references: {
            model: "User",
            key: "user_id",
          },
          field: "user_id",
        },
        fileReference: {
          type: DataTypes.STRING(255),
          allowNull: true,
          field: "file_reference",
        },
        data: {
          type: DataTypes.BLOB,
          allowNull: true,
        },
        fileType: {
          type: DataTypes.STRING(255),
          allowNull: true,
          field: "file_type",
        },
        fileName: {
          type: DataTypes.STRING(255),
          allowNull: true,
          field: "file_name",
        },
        sector: {
          type: DataTypes.STRING(255),
          allowNull: true,
        },
        url: {
          type: DataTypes.STRING(255),
          allowNull: true,
        },
        status: {
          type: DataTypes.STRING(255),
          allowNull: true,
        },
        gpcRefNo: {
          type: DataTypes.STRING(255),
          allowNull: true,
          field: "gpc_ref_no",
        },
        lastUpdated: {
          type: DataTypes.DATE,
          field: "last_updated",
        },
      },
      {
        sequelize,
        underscored: true,
        tableName: "UserFile",
        schema: "public",
        timestamps: true,
        createdAt: "created",
        updatedAt: "last_updated",
        indexes: [
          {
            name: "UserFile_pkey",
            unique: true,
            fields: [{ name: "id" }],
          },
        ],
      },
    );
  }
}